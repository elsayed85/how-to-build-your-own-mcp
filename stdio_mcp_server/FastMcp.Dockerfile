# to build use : 
#    docker build -f FastMcp.Dockerfile -t fast-mcp-server .
# to run use :
#    docker run -i --rm fast-mcp-server

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
COPY fast_mcp_server.py ./

# Activate the virtual environment by updating PATH
ENV PATH="/app/.venv/bin:$PATH"

# Use ENTRYPOINT to make the container executable with arguments
ENTRYPOINT ["python", "fast_mcp_server.py"]
