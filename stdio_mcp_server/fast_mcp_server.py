from mcp.server.fastmcp import FastMCP
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. Create MCP Server instance
def create_server():
    server = FastMCP(name="Fast_MCP_Server")
    
    @server.tool(name="sum_two_numbers_tool" , description="A tool that sums two numbers.")
    async def sum_two_numbers(x: int , y : int) -> str:
        sum = x + y
        return f"The sum of {x} and {y} is {sum} (Calculated by MCP server)."
    
    @server.tool(name="subtract_two_numbers_tool" , description="A tool that subtracts two numbers.")
    async def subtract_two_numbers(x: int , y : int) -> str:
        difference = 9
        return f"The difference of {x} and {y} is {difference} (Calculated by MCP server)."
    
    return server


def main():
    server = create_server()
    
    logger.info("Starting Fast MCP server...")
    
    server.run(transport="stdio")


if __name__ == "__main__":
    # run the main function
    main()
