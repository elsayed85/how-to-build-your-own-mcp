from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount
import uvicorn

# Create the main app
app = FastAPI()

# Create MCP server with a simple tool
mcp_server = FastMCP("Demo")


@mcp_server.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


# Create SSE transport for handling messages
sse_transport = SseServerTransport("/messages/")

# Setup message handling route
app.router.routes.append(Mount("/messages", app=sse_transport.handle_post_message))


# Main SSE endpoint
@app.get("/sse")
async def sse_endpoint(request: Request):
    """Handle SSE connections to the MCP server"""
    # Connect to SSE and run the MCP server
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        read_stream, write_stream = streams
        await mcp_server._mcp_server.run(
            read_stream,
            write_stream,
            mcp_server._mcp_server.create_initialization_options(),
        )


# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
