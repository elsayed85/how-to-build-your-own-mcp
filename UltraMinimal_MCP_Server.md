# ⚡ Ultra Minimal MCP Server Architecture

## Overview
The Ultra Minimal MCP Server is the simplest possible MCP implementation, providing a basic calculator function using standard MCP library with stdio transport.

---

## 🏗️ Minimal Server Architecture

```mermaid
graph TB
    subgraph "Ultra Minimal MCP Server"
        direction TB
        A[MCP Server<br/>calculator] --> B[stdio Transport Layer]
        B --> C[Tool Registry<br/>Single Tool]
        
        C --> D[sum_two_numbers]
        D --> E[Simple Addition Logic<br/>arguments.a + arguments.b]
        E --> F[TextContent Response<br/>Plain text result]
    end
    
    subgraph "Standard MCP Components"
        G[Server Class] --> H[list_tools Decorator]
        G --> I[call_tool Decorator] 
        H --> J[Tool Schema Definition]
        I --> K[Tool Execution Handler]
    end
    
    A --> G
    
    classDef minimal fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef transport fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef tool fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef standard fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A,B,C minimal
    class D,E,F transport
    class G,H,I,J,K standard
```

---

## 🔧 Code Structure Breakdown

```mermaid
graph LR
    subgraph "Imports & Setup"
        A1[asyncio] --> A2[Core async runtime]
        B1[logging] --> B2[Basic logging setup]  
        C1[mcp.server] --> C2[Server, stdio_server]
        D1[mcp.types] --> D2[Tool, TextContent]
    end
    
    subgraph "Server Configuration"
        E1[Server Instance] --> E2[Server name: calculator]
        F1[Logger Setup] --> F2[INFO level logging]
    end
    
    subgraph "Tool Implementation"
        G1["@server.list_tools"] --> G2[Return tool definitions]
        H1["@server.call_tool"] --> H2[Handle tool execution]
        I1[Tool Schema] --> I2[JSON Schema validation]
    end
    
    classDef imports fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef config fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef implementation fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A1,A2,B1,B2,C1,C2,D1,D2 imports
    class E1,E2,F1,F2 config
    class G1,G2,H1,H2,I1,I2 implementation
```

---

## 🔄 Stdio Transport Communication

```mermaid
sequenceDiagram
    participant Client Process
    participant stdio_server
    participant MCP Server
    participant Tool Handler
    
    Note over Client Process,Tool Handler: Standard Input/Output Communication
    
    Client Process->>stdio_server: Initialize connection via stdin/stdout
    stdio_server->>MCP Server: Create read/write streams
    MCP Server->>stdio_server: Initialization options
    stdio_server->>Client Process: Connection established
    
    Client Process->>stdio_server: List tools request (JSON)
    stdio_server->>MCP Server: Parse and forward request  
    MCP Server->>MCP Server: Call @list_tools handler
    MCP Server->>stdio_server: Tools list response
    stdio_server->>Client Process: JSON response via stdout
    
    Client Process->>stdio_server: Call tool: sum_two_numbers(5, 3)
    stdio_server->>MCP Server: Parse tool call request
    MCP Server->>Tool Handler: Execute sum_two_numbers
    Tool Handler->>Tool Handler: Calculate 5 + 3 = 8
    Tool Handler->>MCP Server: Return TextContent result
    MCP Server->>stdio_server: Tool response
    stdio_server->>Client Process: JSON result via stdout
```

---

## 📋 Tool Schema Definition

```mermaid
graph TD
    subgraph "Tool Schema Structure"
        A[Tool Definition] --> B[name: sum_two_numbers]
        A --> C[description: Add two numbers together]
        A --> D[inputSchema]
        
        D --> E[type: object]
        D --> F[properties]
        D --> G["required: [a, b]"]
        
        F --> H[a: type number<br/>description: First number]
        F --> I[b: type number<br/>description: Second number]
    end
    
    subgraph "Validation Flow"
        J[Client Input] --> K[JSON Schema Validation]
        K --> L{Valid?}
        L -->|Yes| M[Execute Tool]
        L -->|No| N[Return Validation Error]
    end
    
    classDef schema fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef validation fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef flow fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A,B,C,D,E,F,G,H,I schema
    class J,K,L validation
    class M,N flow
```


---

## 📋 Quick Commands

### Direct Execution
```bash
# Run the server directly
uv run python ultra_minimal_server.py

# With explicit python version
python3 ultra_minimal_server.py

# With virtual environment
source .venv/bin/activate && python ultra_minimal_server.py
```

### Testing with MCP Client
```bash
# Using the included client
cd ../mcp_client
uv run python client.py ../stdio_mcp_server/ultra_minimal_server.py
```

### Tool Usage Example
```json
{
  "method": "tools/call",
  "params": {
    "name": "sum_two_numbers",
    "arguments": {
      "a": 15,
      "b": 27
    }
  }
}

// Response:
{
  "result": [
    {
      "type": "text", 
      "text": "The sum of 15 and 27 is 42 (Calculated by MCP server)."
    }
  ]
}
```

---

## 🔍 Code Comparison: Minimal vs FastMCP

```mermaid
graph LR
    subgraph "Ultra Minimal (Standard MCP)"
        A1[Server Class] --> A2[Manual decorators]
        A2 --> A3[Explicit stdio setup]
        A3 --> A4[Manual schema definition]
        A4 --> A5[TextContent responses]
    end
    
    subgraph "FastMCP Alternative"
        B1[FastMCP Class] --> B2[Automatic decorators]
        B2 --> B3[Transport auto-detection]
        B3 --> B4[Type-based schemas]
        B4 --> B5[Auto response formatting]
    end
    
    classDef minimal fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef fast fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    
    class A1,A2,A3,A4,A5 minimal
    class B1,B2,B3,B4,B5 fast
```

---

## 🎯 Key Features

- 🎯 **Absolute Simplicity**: Minimal code, maximum clarity
- 📚 **Educational Focus**: Perfect for learning MCP concepts
- 🔧 **Standard Library**: Uses core MCP without abstractions
- 📡 **stdio Transport**: Standard input/output communication
- ✅ **Schema Validation**: Proper input validation with JSON Schema
- 🛡️ **Error Handling**: Basic error handling for unknown tools
- 📝 **Clear Logging**: Informative logging for debugging
- 🚀 **Async Ready**: Fully asynchronous implementation
- 🔒 **Type Safety**: Proper type hints and validation
- 📦 **Zero Dependencies**: Only uses core MCP library

---

## 💡 Learning Objectives

This minimal server teaches:
- Basic MCP server structure
- Tool registration patterns
- Schema definition requirements
- stdio transport usage
- Async/await patterns
- Error handling basics
- Logging best practices

---

*Ultra Minimal MCP Server - The perfect starting point for MCP development! ⚡*
