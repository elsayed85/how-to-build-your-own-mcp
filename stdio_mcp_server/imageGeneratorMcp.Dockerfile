# to build use : 
#    docker build -f imageGeneratorMcp.Dockerfile -t image-generator-mcp-server .
# to run use :
#    docker run -i --rm image-generator-mcp-server

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
COPY image_generator_mcp_server.py ./

# Activate the virtual environment by updating PATH
ENV PATH="/app/.venv/bin:$PATH"

# Use ENTRYPOINT to make the container executable with arguments
ENTRYPOINT ["python", "image_generator_mcp_server.py"]
