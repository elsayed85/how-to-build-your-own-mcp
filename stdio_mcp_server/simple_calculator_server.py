#!/usr/bin/env python3
"""
Simple Calculator MCP Server for Live Stream Demo
=================================================

This is a proper stdio MCP server that works with the minimal example.
It provides basic math operations: add, subtract, multiply, divide.
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the server
server = Server("simple-calculator")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available calculator tools."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract second number from first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number (dividend)"},
                    "b": {"type": "number", "description": "Second number (divisor)"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")

    if name == "add":
        result = arguments["a"] + arguments["b"]
        return [TextContent(type="text", text=f"{result}")]

    elif name == "subtract":
        result = arguments["a"] - arguments["b"]
        return [TextContent(type="text", text=f"{result}")]

    elif name == "multiply":
        result = arguments["a"] * arguments["b"]
        return [TextContent(type="text", text=f"{result}")]

    elif name == "divide":
        if arguments["b"] == 0:
            return [TextContent(type="text", text="Error: Cannot divide by zero")]
        result = arguments["a"] / arguments["b"]
        return [TextContent(type="text", text=f"{result}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


def main():
    """Run the calculator server."""
    logger.info("Starting Simple Calculator MCP Server...")

    async def run_server():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
