from mcp.server.fastmcp import FastMCP
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    # 1. Create a FastMCP server instance
    mcp = FastMCP(name="Calculator_MCP_Server")

    # 2. Define a tool that sums two numbers
    @mcp.tool(
        name="sum_two_numbers",
        description="A tool that sums two numbers.",
    )
    async def sum_two_numbers_tool(a: int, b: int) -> str:
        """A tool that sums two numbers."""
        return f"The sum of {a} and {b} is {a + b} (Calculated by MCP server)."

    @mcp.tool(
        name="subtract_two_numbers",
        description="A tool that subtracts two numbers.",
    )
    async def subtract_two_numbers_tool(a: int, b: int) -> str:
        """A tool that subtracts two numbers."""
        return f"The difference of {a} and {b} is {a - b} (Calculated by MCP server)."

    @mcp.tool(
        name="multiply_two_numbers",
        description="A tool that multiplies two numbers.",
    )
    async def multiply_two_numbers_tool(a: int, b: int) -> str:
        """A tool that multiplies two numbers."""
        return f"The product of {a} and {b} is {a * b} (Calculated by MCP server)."

    return mcp


def main():
    async def _run():
        server = await serve()
        logger.info("Starting Calculator MCP server...")
        return server

    server = asyncio.run(_run())
    server.run()  # This should work with stdio


if __name__ == "__main__":
    main()
