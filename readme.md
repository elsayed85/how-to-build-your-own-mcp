## Install UV Tool 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create New Project With MCP Library
```bash
# Create project
uv init stdio_mcp_server --bare

# Change to project directory
cd stdio_mcp_server
# Install MCP
uv add "mcp[cli]"

# create main.py file
touch main.py
```


```python
from mcp.server.fastmcp import FastMCP
import asyncio

# 1. Create a FastMCP server instance
mcp = FastMCP(
    name="sum_two_numbers_mcp_server",
)

# 2. Define a tool that sums two numbers
@mcp.tool(
    name="sum_two_numbers",
    description="A tool that sums two numbers.",
)
async def sum_two_numbers_tool(a: int, b: int) -> int:
    """A tool that sums two numbers."""
    return f"The sum of {a} and {b} is {a + b} (Calculated by MCP server)."


if __name__ == "__main__":
    # 3. Run the FastMCP server
    asyncio.run(mcp.run())


# 4. Run with : python main.py
```
