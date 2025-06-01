import asyncio
import sys
import logging
import json
import re

from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

from openai import AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()

# Set up logger
logger = logging.getLogger(__name__)

# Create formatters
detailed_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_formatter = logging.Formatter("%(levelname)s: %(message)s")

# File handler for detailed logs (including MCP payloads)
file_handler = logging.FileHandler("logs/mcp_client.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

# Console handler for essential info only
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Only show warnings and errors in console
console_handler.setFormatter(console_formatter)

# Configure root logger
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Create a separate logger for MCP payloads that only goes to file
mcp_payload_logger = logging.getLogger("mcp_payloads")
mcp_payload_logger.setLevel(logging.INFO)
mcp_payload_file_handler = logging.FileHandler("logs/mcp_payloads.log")
mcp_payload_file_handler.setFormatter(detailed_formatter)
mcp_payload_logger.addHandler(mcp_payload_file_handler)
mcp_payload_logger.propagate = False  # Don't propagate to parent logger


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = AsyncOpenAI()
        self.cached_tools = None  # Cache for available tools

        logger.info("Initialized MCPClient with OpenAI as the LLM provider")

    async def connect_to_sse_server(self, server_url: str):
        """Connect to an SSE MCP server.

        Args:
            server_url (str): URL of the SSE MCP server.
        """
        logger.debug(f"Connecting to SSE MCP server at {server_url}")

        # Store the context managers so they stay alive
        self._streams_context = sse_client(url=server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # Load and cache tools
        await self._load_and_cache_tools()
        
        print(f"Connected to SSE MCP Server at {server_url}")
        print(f"Available tools: {[tool['name'] for tool in self.cached_tools]}")
        logger.info(
            f"Connected to SSE MCP Server at {server_url}. Available tools: {[tool['name'] for tool in self.cached_tools]}"
        )

    async def connect_to_stdio_server(self, server_script_path: str, server_args: list = None):
        """Connect to a stdio MCP server.

        Args:
            server_script_path (str): Path to the server script (.py, .js, or npm package).
            server_args (list, optional): Additional arguments to pass to the server.
        """
        is_python = False
        is_javascript = False
        command = None
        args = [server_script_path]
        
        # Add any additional server arguments
        if server_args:
            args.extend(server_args)

        # Determine if the server is a file path or npm package
        if server_script_path.startswith("@") or "/" not in server_script_path:
            # Assume it's an npm package
            is_javascript = True
            command = "npx"
        else:
            # It's a file path
            is_python = server_script_path.endswith(".py")
            is_javascript = server_script_path.endswith(".js")
            if not (is_python or is_javascript):
                raise ValueError(
                    "Server script must be a .py, .js file or npm package."
                )

            command = "python" if is_python else "node"

        server_params = StdioServerParameters(command=command, args=args, env=None)

        logger.debug(
            f"\n\nConnecting to stdio MCP server with command: {command} and args: {args}"
        )

        # Start the server
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.writer = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.writer)
        )

        await self.session.initialize()

        # Load and cache tools
        await self._load_and_cache_tools()
        
        print("Connected to stdio MCP Server")
        print(f"Available tools: {[tool['name'] for tool in self.cached_tools]}")
        logger.info(
            f"Connected to stdio MCP Server. Available tools: {[tool['name'] for tool in self.cached_tools]}"
        )

    async def connect_to_server(self, server_path_or_url: str, server_args: list = None):
        """Connect to an MCP server (either stdio or SSE).

        Args:
            server_path_or_url (str): Path to the server script or URL of SSE server.
            server_args (list, optional): Additional arguments to pass to stdio servers.
        """
        # Check if the input is a URL (for SSE server)
        url_pattern = re.compile(r"^https?://")

        if url_pattern.match(server_path_or_url):
            # It's a URL, connect to SSE server
            await self.connect_to_sse_server(server_path_or_url)
        else:
            # It's a script path, connect to stdio server
            await self.connect_to_stdio_server(server_path_or_url, server_args)

    async def process_query(
        self, query: str, previous_messages: list = None
    ) -> tuple[str, list]:
        """Process a query using the MCP server and available tools.

        Args:
            query (str): The query to send to the server.
            previous_messages (list, optional): Previous conversation history.

        Returns:
            tuple[str, list]: The response from the server and updated messages.
        """
        if not self.session:
            raise RuntimeError("Client session is not initialized.")

        # Use cached tools instead of fetching them every time
        if self.cached_tools is None:
            raise RuntimeError("Tools not cached. Make sure to connect to server first.")

        return await self._process_query_openai(
            query, self.cached_tools, previous_messages
        )

    async def _process_query_openai(
        self, query: str, available_tools: list, previous_messages: list = None
    ) -> tuple[str, list]:
        """Process a query using OpenAI's GPT models."""
        model = "gpt-4o"

        # Convert available_tools to OpenAI format
        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"],
                },
            }
            for tool in available_tools
        ]

        messages = []
        if previous_messages:
            messages.extend(previous_messages)

        messages.append({"role": "user", "content": query})

        mcp_payload_logger.info("=" * 50)
        mcp_payload_logger.info("OPENAI REQUEST PAYLOAD:")
        mcp_payload_logger.info(f"Model: {model}")
        try:
            mcp_payload_logger.info(f"Messages: {json.dumps(messages, indent=2, default=str)}")
        except Exception:
            mcp_payload_logger.info(f"Messages: {str(messages)}")
        mcp_payload_logger.info(f"Tools: {json.dumps(openai_tools, indent=2)}")
        mcp_payload_logger.info("=" * 50)

        logger.debug("Messages sent to OpenAI: %s", messages)
        logger.debug("Available tools: %s", openai_tools)

        # Initialize OpenAI API call
        print(f"Sending query to {model}...")
        logger.info(f"Sending query to {model}...")
        response = await self.openai.chat.completions.create(
            model=model, messages=messages, tools=openai_tools, tool_choice="auto"
        )

        response_message = response.choices[0].message
        
        mcp_payload_logger.info("=" * 50)
        mcp_payload_logger.info("OPENAI RESPONSE PAYLOAD:")
        mcp_payload_logger.info(f"Content: {response_message.content}")
        mcp_payload_logger.info(f"Tool Calls: {response_message.tool_calls}")
        mcp_payload_logger.info("=" * 50)
        
        final_text = []

        # Process tool calls if any
        if response_message.tool_calls:
            final_text.append(response_message.content or "")

            # Add the assistant's response to messages
            messages.append(
                {
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": response_message.tool_calls,
                }
            )

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Log the MCP request payload
                mcp_payload_logger.info("=" * 50)
                mcp_payload_logger.info("MCP TOOL REQUEST PAYLOAD:")
                mcp_payload_logger.info(f"Tool Name: {function_name}")
                mcp_payload_logger.info(f"Tool Arguments: {json.dumps(function_args, indent=2)}")
                mcp_payload_logger.info("=" * 50)

                # Execute tool call
                logger.debug(
                    f"Calling tool {function_name} with args {function_args}..."
                )
                final_text.append(
                    f"[Calling tool {function_name} with args {function_args}]"
                )
                result = await self.session.call_tool(function_name, function_args)
                
                # Log the MCP response payload
                mcp_payload_logger.info("=" * 50)
                mcp_payload_logger.info("MCP TOOL RESPONSE PAYLOAD:")
                mcp_payload_logger.info(f"Result Meta: {result.meta}")
                mcp_payload_logger.info(f"Result Content: {result.content}")
                mcp_payload_logger.info(f"Is Error: {result.isError}")
                mcp_payload_logger.info("=" * 50)
                
                final_text.append(f"[tool results: {result}]")

                # Add tool result to messages
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content,
                    }
                )

            # Get the final response after tool calls
            logger.debug("Getting next response from OpenAI...")
            next_response = await self.openai.chat.completions.create(
                model=model, messages=messages
            )

            logger.debug("Response from OpenAI: %s", next_response.choices[0].message)
            final_text.append(next_response.choices[0].message.content)
            messages.append(
                {
                    "role": "assistant",
                    "content": next_response.choices[0].message.content,
                }
            )
        else:
            final_text.append(response_message.content)

        return "\n".join(final_text), messages

    async def chat_loop(self):
        """Run an interactive chat loop with the server."""
        previous_messages = []
        print("Type your queries or 'quit' to exit.")
        print("Type 'refresh' to clear conversation history.")
        print("Type 'refresh-tools' to reload tools from the server.")
        print("Using OpenAI as the LLM provider.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break

                #  Check if the user wants to refresh conversation (history)
                if query.lower() == "refresh":
                    previous_messages = []
                    print("Conversation history cleared.")
                    continue

                # Check if the user wants to refresh tools cache
                if query.lower() == "refresh-tools":
                    try:
                        await self.refresh_tools_cache()
                        print("Tools cache refreshed successfully.")
                        print(f"Available tools: {[tool['name'] for tool in self.cached_tools]}")
                    except Exception as e:
                        print(f"Failed to refresh tools cache: {str(e)}")
                    continue

                response, previous_messages = await self.process_query(
                    query, previous_messages=previous_messages
                )
                print("\nResponse:", response)
            except Exception as e:
                logger.exception("Error in chat loop")
                print("Error:", str(e))

    async def clenup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()
        if hasattr(self, "_session_context") and self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if hasattr(self, "_streams_context") and self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

    async def _load_and_cache_tools(self):
        """Load tools from the MCP server and cache them."""
        if not self.session:
            raise RuntimeError("Client session is not initialized.")
        
        mcp_payload_logger.info("=" * 50)
        mcp_payload_logger.info("MCP LIST TOOLS REQUEST (INITIAL LOAD)")
        mcp_payload_logger.info("=" * 50)
        response = await self.session.list_tools()
        mcp_payload_logger.info("=" * 50)
        mcp_payload_logger.info("MCP LIST TOOLS RESPONSE (INITIAL LOAD):")
        mcp_payload_logger.info(f"Available tools: {[tool.name for tool in response.tools]}")
        for tool in response.tools:
            mcp_payload_logger.info(f"Tool: {tool.name}")
            mcp_payload_logger.info(f"  Description: {tool.description}")
            mcp_payload_logger.info(f"  Input Schema: {tool.inputSchema}")
        mcp_payload_logger.info("=" * 50)
        
        # Cache the tools in the format needed for OpenAI
        self.cached_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": dict(tool.inputSchema) if tool.inputSchema else {},
            }
            for tool in response.tools
        ]
        
        logger.info(f"Cached {len(self.cached_tools)} tools")

    async def refresh_tools_cache(self):
        """Refresh the cached tools by fetching them again from the server."""
        logger.info("Refreshing tools cache...")
        await self._load_and_cache_tools()
        logger.info("Tools cache refreshed successfully")


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_script_path_or_url> [server_args...]")
        print("Examples:")
        print("  - stdio server (npm): python client.py @playwright/mcp@latest")
        print("  - stdio server (python): python client.py ./weather.py")
        print("  - stdio server with args: python client.py ./dev_blog_server.py --auth-token YOUR_TOKEN")
        print("  - SSE server: python client.py http://localhost:3000/mcp")
        sys.exit(1)

    server_path_or_url = sys.argv[1]
    server_args = sys.argv[2:] if len(sys.argv) > 2 else None

    client = MCPClient()
    try:
        await client.connect_to_server(server_path_or_url, server_args)
        await client.chat_loop()
    finally:
        await client.clenup()
        print("\nMCP Client Closed!")


def cli_main():
    """Synchronous entry point for the CLI."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
