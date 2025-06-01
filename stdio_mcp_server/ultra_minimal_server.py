#!/usr/bin/env python3
"""
Ultra Minimal Calculator MCP Server
===================================

This is the simplest possible MCP server that works with stdio transport.
Based on the official MCP Python examples.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create server
server = Server("calculator")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List calculator tools."""
    return [
        Tool(
            name="sum_two_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "sum_two_numbers":
        result = arguments["a"] + arguments["b"]
        return [
            TextContent(
                type="text",
                text=f"The sum of {arguments['a']} and {arguments['b']} is {result} (Calculated by MCP server).",
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the server using stdio transport."""
    logger.info("Starting Ultra Minimal Calculator MCP Server...")

    # Use stdio_server context manager
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
