from typing import Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


async def serve() -> None:
    server = Server("mcp_server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available time tools."""
        return [
            #
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
        pass

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)


def main() -> None:
    import asyncio

    async def _run() -> None:
        await serve()

    asyncio.run(_run())


if __name__ == "__main__":
    main()
