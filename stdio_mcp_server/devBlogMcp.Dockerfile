# to build use : 
#    docker build -f devBlogMcp.Dockerfile -t dev-to-mcp-server .

# Use Python 3.12 slim image as the base
FROM python:3.12-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy project configuration files first (for better Docker layer caching)
COPY pyproject.toml uv.lock ./

# Install uv package manager
RUN pip install uv

# Install project dependencies using uv
RUN uv sync --frozen --no-dev

# Copy the MCP server Python script
COPY dev_to_search_tool_mcp_server.py ./

# Activate the virtual environment by updating PATH
ENV PATH="/app/.venv/bin:$PATH"

# Use ENTRYPOINT to make the container executable with arguments
ENTRYPOINT ["python", "dev_to_search_tool_mcp_server.py"]
