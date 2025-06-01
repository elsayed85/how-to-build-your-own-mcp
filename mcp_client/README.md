# MCP Client

A simple MCP (Model Context Protocol) client that connects to MCP servers and uses OpenAI for processing queries.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up your OpenAI API key in a `.env` file:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Usage

Run the client with a server:

```bash
# With a stdio server (npm package)
uv run python client.py @playwright/mcp@latest

# With a stdio server (Python script)
uv run python client.py ./weather.py

# With an SSE server
uv run python client.py http://localhost:3000/mcp
```

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol library
- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management

## Features

- Connect to both stdio and SSE MCP servers
- Interactive chat loop with conversation history
- Tool calling support through OpenAI
- Comprehensive logging
