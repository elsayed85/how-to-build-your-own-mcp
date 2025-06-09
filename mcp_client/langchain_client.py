import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from logging_utils import create_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = create_logger()

mcp_dir = os.path.dirname(os.path.abspath(__file__)) + "/../stdio_mcp_server"
dev_blog_auth_token = os.getenv("DEV_BLOG_AUTH_TOKEN", "")

print(f"Using MCP directory: {mcp_dir}")

server_config = {
    "math": {
        "command": "python",
        "args": [f"{mcp_dir}/calculator_mcp_server.py"],
        "transport": "stdio",
    },
    "image-generation": {
        "command": "python",
        "args": [f"{mcp_dir}/image_generator_mcp_server.py"],
        "transport": "stdio",
    },
    "dev-blog": {
        "command": "python",
        "args": [
            f"{mcp_dir}/dev_blog_mcp_server.py",
            "--auth-token",
            dev_blog_auth_token,
        ],
        "transport": "stdio",
    },
}


def create_mcp_client() -> MultiServerMCPClient:
    """Initialize and configure the MCP client with server connections."""
    logger.log_step(2, "Initializing MCP Client...")

    try:
        client = MultiServerMCPClient(server_config)
        logger.log_success("MCP Client initialized successfully")
        logger.log_info("  - Math server: stdio_mcp_server/calculator_mcp_server.py")
        return client
    except Exception as e:
        logger.log_error("Failed to initialize MCP Client", e)
        raise


async def discover_available_tools(client: MultiServerMCPClient) -> list:
    """Retrieve and log all available tools from MCP servers."""
    logger.log_step(3, "Retrieving available tools from MCP servers...")

    try:
        tools = await client.get_tools()
        logger.log_success(f"Successfully retrieved {len(tools)} tools")
        for i, tool in enumerate(tools, 1):
            logger.log_info(f"  Tool {i}: {tool.name} - {tool.description}")
        return tools
    except Exception as e:
        logger.log_error("Failed to get tools", e)
        raise


def create_langchain_agent(tools: list, model_name: str = "gpt-4o-mini"):
    """Create a React agent with the specified model and tools."""
    logger.log_step(4, f"Creating React Agent with {model_name}...")

    try:
        agent = create_react_agent(
            model=model_name,
            tools=tools,
            prompt="You are a helpful assistant that can use tools to answer questions.",
            debug=False,
        )
        logger.log_success("React Agent created successfully")
        logger.log_info(f"  - Model: {model_name}")
        logger.log_info(f"  - Tools attached: {len(tools)}")
        return agent
    except Exception as e:
        logger.log_error("Failed to create React Agent", e)
        raise


async def execute_query(
    agent, query: str, conversation_history: list, query_number: int = 1
):
    """Execute a query using the agent with conversation history and return the response."""
    logger.log_query_start(query_number, query, len(conversation_history))

    try:
        # Add the new user message to conversation history
        conversation_history.append({"role": "user", "content": query})

        logger.log_info("Sending request to agent with conversation history...")
        response = await agent.ainvoke({"messages": conversation_history})

        # Update conversation history with the complete response messages
        if "messages" in response:
            # Replace conversation history with the complete updated conversation
            # This includes all the intermediate tool calls and responses
            conversation_history.clear()
            conversation_history.extend(response["messages"])
            logger.log_query_success(len(conversation_history))

        return response
    except Exception as e:
        logger.log_error("Failed to execute query", e)
        raise


def analyze_conversation_flow(response, query_number: int = 1):
    """Parse and log the conversation flow from the agent response."""
    messages = response.get("messages", [])
    logger.log_response_analysis(query_number, str(type(response)), len(messages))

    logger.log_conversation_flow_header()

    for i, message in enumerate(messages, 1):
        message_type = message.__class__.__name__
        content = (
            message.content if hasattr(message, "content") and message.content else None
        )
        tool_calls = (
            message.tool_calls
            if hasattr(message, "tool_calls") and message.tool_calls
            else None
        )
        tool_name = message.name if hasattr(message, "name") and message.name else None
        tool_result = (
            message.content if hasattr(message, "content") and tool_name else None
        )

        logger.log_message_details(
            i, message_type, content, tool_calls, tool_name, tool_result
        )

    return messages


def display_final_results(messages: list, original_query: str, query_number: int = 1):
    """Extract and display the final answer in a clean format."""
    final_message = messages[-1] if messages else None

    if final_message and hasattr(final_message, "content"):
        logger.log_final_answer(query_number, final_message.content)

        print("\n" + "=" * 60)
        print(f"🎯 CLEAN RESULT SUMMARY #{query_number}:")
        print("=" * 60)
        print(f"Question: {original_query}")
        print(f"Answer: {final_message.content}")
        print("=" * 60)

    # Add separation between queries
    logger.log_query_separation()


async def run_interactive_chat(agent):
    """Run an interactive chat loop where user can send multiple queries."""
    print("\n" + "🚀" * 30)
    print("🤖 INTERACTIVE LANGCHAIN MCP CHAT")
    print("🚀" * 30)
    print("💡 Type your questions and press Enter")
    print("💡 Type 'quit', 'exit', or 'q' to stop")
    print("💡 Type 'help' for available commands")
    print("🚀" * 30 + "\n")

    query_number = 1
    conversation_history = []  # Initialize conversation history

    while True:
        try:
            # Get user input
            user_input = input(f"\n💬 Query #{query_number}: ").strip()

            # Handle special commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye! Chat session ended.")
                logger.log_chat_session_end("user")
                break

            if user_input.lower() == "help":
                print("\n📚 Available commands:")
                print("  - Type any question to get an answer")
                print("  - 'quit', 'exit', 'q' - End the chat")
                print("  - 'help' - Show this help message")
                continue

            if not user_input:
                print("❌ Please enter a question or command")
                continue

            # Execute the query with conversation history
            response = await execute_query(
                agent, user_input, conversation_history, query_number
            )

            # Analyze and display results
            messages = analyze_conversation_flow(response, query_number)
            display_final_results(messages, user_input, query_number)

            # Conversation history is now automatically updated in execute_query
            query_number += 1

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted by user (Ctrl+C)")
            logger.log_chat_session_end("interrupt")
            break
        except Exception as e:
            print(f"\n❌ Error processing query: {e}")
            logger.log_chat_error(str(e))
            continue


async def main():
    """Main function orchestrating the entire langchain MCP client workflow."""
    logger.log_startup()

    try:
        # Step 1: Initialize MCP client
        client = create_mcp_client()

        # Step 2: Discover available tools
        tools = await discover_available_tools(client)

        # Step 3: Create langchain agent
        agent = create_langchain_agent(tools)

        # Step 4: Run interactive chat
        await run_interactive_chat(agent)

    except Exception as e:
        logger.log_error("Application failed", e)
        return

    logger.log_completion()


if __name__ == "__main__":
    asyncio.run(main())
