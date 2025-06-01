# 🎯 Ultra Minimal MCP Server - Practical Examples

## Overview
This document provides educational examples for the Ultra Minimal MCP Server, demonstrating basic MCP concepts and simple tool usage patterns for learning purposes.

---

## 📚 Learning MCP Fundamentals

### Example 1: First MCP Tool Call
```
I'm new to MCP (Model Context Protocol) and want to test a simple tool.
Can you call the 'greet' function with my name "Alice"?

This should demonstrate the basic MCP tool calling mechanism.
```

**Expected MCP Tool Call:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "greet",
    "arguments": {
      "name": "Alice"
    }
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Hello, Alice! Welcome to the Ultra Minimal MCP Server."
    }
  ]
}
```

**Learning Points:**
- Tool name must match exactly: `greet`
- Arguments passed as JSON object
- Simple string parameter handling
- Basic response structure

---

### Example 2: Understanding Tool Discovery
```
Show me what tools are available in this minimal MCP server.
I want to understand how MCP servers expose their capabilities.
```

**MCP Tools List Response:**
```mermaid
graph TD
    A[Ultra Minimal Server] --> B[Available Tools]
    B --> C[greet]
    
    C --> D[Parameters]
    D --> E[name: string<br/>required]
    
    C --> F[Description]
    F --> G["A simple greeting tool that<br/>takes a name and returns<br/>a personalized greeting"]
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef tool fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef param fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef desc fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A,B server
    class C tool
    class D,E param
    class F,G desc
```

**Tool Schema:**
```json
{
  "name": "greet",
  "description": "A simple greeting tool that takes a name and returns a personalized greeting",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "The name of the person to greet"
      }
    },
    "required": ["name"]
  }
}
```

---

## 🎓 Educational Use Cases

### Example 3: MCP Protocol Flow
```
Walk me through what happens when I call the greet function step by step.
I want to understand the complete MCP request/response cycle.
```

**MCP Protocol Flow:**
```mermaid
sequenceDiagram
    participant Client
    participant MCPServer
    participant GreetTool
    
    Client->>MCPServer: tools/list request
    MCPServer->>Client: Available tools response
    
    Client->>MCPServer: tools/call "greet" {"name": "Bob"}
    MCPServer->>GreetTool: Execute with parameters
    GreetTool->>GreetTool: Process name: "Bob"
    GreetTool->>MCPServer: Return: "Hello, Bob! Welcome..."
    MCPServer->>Client: Tool result response
    
    Note over Client,MCPServer: Standard MCP protocol
    Note over MCPServer,GreetTool: Server-specific logic
```

**Step-by-Step Breakdown:**
1. **Tool Discovery**: Client requests available tools
2. **Tool Selection**: Client chooses `greet` tool
3. **Parameter Validation**: Server validates `name` parameter
4. **Tool Execution**: Server runs greeting logic
5. **Response Formation**: Server formats response
6. **Result Return**: Client receives formatted greeting

---

### Example 4: Testing Different Inputs
```
Test the greet function with various inputs to understand parameter handling:
- Normal name: "John"
- Name with spaces: "Mary Jane"  
- Empty string: ""
- Special characters: "José"

Show how the MCP server handles different input types.
```

**Input Validation Testing:**
```mermaid
graph TD
    A[Input Testing] --> B[Valid Inputs]
    A --> C[Edge Cases]
    A --> D[Error Handling]
    
    B --> E["John" → Valid]
    B --> F["Mary Jane" → Valid]
    B --> G["José" → Valid]
    
    C --> H["" → Empty string]
    C --> I["   " → Whitespace only]
    C --> J["123" → Numbers]
    
    D --> K[Missing parameter]
    D --> L[Wrong parameter type]
    D --> M[Extra parameters]
    
    classDef valid fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef edge fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef error fill:#f44336,stroke:#c62828,stroke-width:2px,color:#fff
    
    class A,B,E,F,G valid
    class C,H,I,J edge
    class D,K,L,M error
```

**Test Calls:**
1. `greet("John")` → "Hello, John! Welcome to the Ultra Minimal MCP Server."
2. `greet("Mary Jane")` → "Hello, Mary Jane! Welcome to the Ultra Minimal MCP Server."
3. `greet("")` → "Hello, ! Welcome to the Ultra Minimal MCP Server."
4. `greet("José")` → "Hello, José! Welcome to the Ultra Minimal MCP Server."

---

## 🛠️ Development Learning

### Example 5: MCP Server Architecture
```
Explain how this minimal server is structured and what makes it a good learning example.
Show the code architecture and how it implements the MCP standard.
```

**Server Architecture:**
```mermaid
graph TD
    A[Ultra Minimal Server] --> B[MCP Framework]
    A --> C[Tool Definition]
    A --> D[Main Function]
    
    B --> E[FastMCP Library]
    B --> F[Standard Protocol]
    B --> G[JSON-RPC Transport]
    
    C --> H[greet_tool Function]
    C --> I[Parameter Schema]
    C --> J[Response Format]
    
    D --> K[Server Initialization]
    D --> L[Tool Registration]
    D --> M[Server Start]
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef framework fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef tool fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef main fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A server
    class B,E,F,G framework
    class C,H,I,J tool
    class D,K,L,M main
```

**Key Components:**
- **FastMCP**: Simplified MCP server framework
- **Tool Registration**: Single `greet` function
- **Parameter Validation**: Type checking for `name`
- **Response Handling**: Structured text response
- **Error Management**: Basic error handling

---

### Example 6: Building on the Minimal Example
```
I understand the basic greet function. How would I extend this server to add more tools?
Show me the pattern for adding additional functionality.
```

**Extension Patterns:**
```mermaid
graph LR
    A[Current: greet] --> B[Add: farewell]
    A --> C[Add: count_words]
    A --> D[Add: reverse_text]
    
    subgraph "Tool Pattern"
        E[Function Definition]
        F[Parameter Schema]
        G[Business Logic]
        H[Response Format]
    end
    
    B --> E
    C --> E
    D --> E
    
    classDef current fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef extension fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef pattern fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A current
    class B,C,D extension
    class E,F,G,H pattern
```

**Hypothetical Extensions:**
```python
# Following the same pattern as greet
@app.tool()
def farewell(name: str) -> str:
    """Say goodbye to someone"""
    return f"Goodbye, {name}! Thanks for using the MCP server."

@app.tool()
def count_words(text: str) -> str:
    """Count words in a text string"""
    word_count = len(text.split())
    return f"The text contains {word_count} words."
```

---

## 🧪 Testing & Debugging

### Example 7: MCP Client Testing
```
How do I test this minimal server? Show me how to connect a client and verify the tool works correctly.
```

**Testing Setup:**
```mermaid
graph TD
    A[Testing Environment] --> B[Start Server]
    A --> C[Connect Client]
    A --> D[Run Tests]
    
    B --> E[stdio_mcp_server/<br/>ultra_minimal_server.py]
    C --> F[mcp_client/<br/>client.py]
    D --> G[Tool Discovery]
    D --> H[Tool Execution]
    D --> I[Response Validation]
    
    G --> J[List available tools]
    H --> K[Call greet function]
    I --> L[Verify output format]
    
    classDef env fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef setup fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef test fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef verify fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A env
    class B,C,E,F setup
    class D,G,H,J,K test
    class I,L verify
```

**Testing Commands:**
```bash
# Terminal 1: Start the server
cd /Users/elsayed/side-projects/sessions/stdio_mcp_server
uv run python ultra_minimal_server.py

# Terminal 2: Connect client and test
cd ../mcp_client
uv run python client.py ../stdio_mcp_server/ultra_minimal_server.py

# Interactive testing:
> list_tools
> greet Alice
> greet "John Doe"
> greet ""
```

---

### Example 8: Error Handling Demonstration
```
Show me what happens when I make invalid requests to the minimal server.
This will help me understand MCP error handling.
```

**Error Scenarios:**
```mermaid
graph TD
    A[Error Testing] --> B[Missing Parameters]
    A --> C[Wrong Parameter Types]
    A --> D[Invalid Tool Names]
    A --> E[Malformed Requests]
    
    B --> F[Call greet without name]
    C --> G[Pass number instead of string]
    D --> H[Call non-existent tool]
    E --> I[Invalid JSON format]
    
    F --> J[Parameter validation error]
    G --> K[Type mismatch error]
    H --> L[Tool not found error]
    I --> M[Protocol error]
    
    classDef test fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef scenario fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef error fill:#f44336,stroke:#c62828,stroke-width:2px,color:#fff
    
    class A test
    class B,C,D,E,F,G,H,I scenario
    class J,K,L,M error
```

**Error Examples:**
1. **Missing Parameter**: `greet()` without name
2. **Wrong Type**: `greet(123)` number instead of string  
3. **Unknown Tool**: `unknown_tool("test")`
4. **Extra Parameters**: `greet("Alice", "extra")`

---

## 🎯 MCP Concepts Demonstrated

### Example 9: Protocol Standards
```
What MCP protocol standards does this minimal server demonstrate?
Help me understand the core MCP concepts through this simple example.
```

**MCP Standards Shown:**
```mermaid
graph TD
    A[MCP Protocol Standards] --> B[Transport Layer]
    A --> C[Tool System]
    A --> D[Type Safety]
    A --> E[Error Handling]
    
    B --> F[STDIO Transport]
    B --> G[JSON-RPC Messages]
    
    C --> H[Tool Discovery]
    C --> I[Tool Calling]
    C --> J[Result Format]
    
    D --> K[Parameter Schemas]
    D --> L[Type Validation]
    
    E --> M[Error Responses]
    E --> N[Status Codes]
    
    classDef standard fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef transport fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef tool fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef type fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef error fill:#f44336,stroke:#c62828,stroke-width:2px,color:#fff
    
    class A standard
    class B,F,G transport
    class C,H,I,J tool
    class D,K,L type
    class E,M,N error
```

**Core Concepts:**
- **Transport**: STDIO-based communication
- **Discovery**: `tools/list` for capability exposure
- **Execution**: `tools/call` for function invocation
- **Schemas**: JSON Schema for parameter validation
- **Responses**: Structured result formatting

---

### Example 10: Learning Path
```
I've mastered this minimal server. What should I learn next in the MCP ecosystem?
Guide me through the progression from this simple example to more complex servers.
```

**MCP Learning Progression:**
```mermaid
graph LR
    A[Ultra Minimal<br/>greet function] --> B[Calculator<br/>math operations]
    B --> C[Image Generator<br/>external APIs]
    C --> D[Dev Blog<br/>CRUD operations]
    D --> E[SSE Server<br/>HTTP transport]
    
    A --> F[Concepts Learned]
    F --> G[Tool calling]
    F --> H[Parameter handling]
    F --> I[Basic responses]
    
    B --> J[Multiple tools]
    B --> K[Number handling]
    B --> L[Error cases]
    
    C --> M[External integration]
    C --> N[URL generation]
    C --> O[Option handling]
    
    D --> P[Complex workflows]
    D --> Q[Authentication]
    D --> R[CRUD patterns]
    
    E --> S[HTTP transport]
    E --> T[REST endpoints]
    E --> U[Server deployment]
    
    classDef minimal fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef intermediate fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef advanced fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef expert fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef concept fill:#607D8B,stroke:#37474F,stroke-width:2px,color:#fff
    
    class A,F,G,H,I minimal
    class B,J,K,L intermediate
    class C,M,N,O advanced
    class D,P,Q,R expert
    class E,S,T,U concept
```

**Next Steps:**
1. **Calculator Server**: Learn multiple tools and data types
2. **Image Generator**: Understand external API integration
3. **Dev Blog Server**: Master complex workflows and authentication
4. **SSE Server**: Explore HTTP-based MCP transport
5. **Custom Server**: Build your own MCP server from scratch

---

## 🔧 Ultra Minimal Server Features

```mermaid
graph TD
    subgraph "Core Features"
        A[Single Tool: greet] --> B[String Parameter]
        B --> C[Text Response]
    end
    
    subgraph "Educational Value"
        D[MCP Basics] --> E[Tool Discovery]
        D --> F[Parameter Validation]
        D --> G[Response Format]
    end
    
    subgraph "Learning Benefits"
        H[Simple to Understand] --> I[Clear Code Structure]
        H --> J[Minimal Dependencies]
        H --> K[Fast Setup]
    end
    
    subgraph "Foundation For"
        L[More Complex Servers] --> M[Additional Tools]
        L --> N[External APIs]
        L --> O[Advanced Features]
    end
    
    classDef feature fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef educational fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef benefit fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef foundation fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A,B,C feature
    class D,E,F,G educational
    class H,I,J,K benefit
    class L,M,N,O foundation
```

---

## 🚀 Quick Start Guide

```bash
# Clone and setup the project
git clone <repository>
cd stdio_mcp_server

# Install dependencies
uv sync

# Start the ultra minimal server
uv run python ultra_minimal_server.py

# In another terminal, connect the client
cd ../mcp_client
uv run python client.py ../stdio_mcp_server/ultra_minimal_server.py

# Try these commands:
> list_tools                    # See available tools
> greet "World"                 # Test the greet function
> greet "Your Name"             # Personalized greeting
> help                          # Client help
> quit                          # Exit the client
```

---

## 💡 Educational Tips

### For Beginners:
- **Start Here**: Perfect first MCP server to understand
- **Simple Code**: Easy to read and modify
- **Clear Purpose**: One tool, one function, clear result
- **Foundation**: Building block for more complex servers

### For Educators:
- **Teaching Tool**: Demonstrate MCP concepts clearly
- **Extensible**: Easy to add new tools for exercises
- **Debuggable**: Simple enough to step through code
- **Standards**: Shows proper MCP implementation

### For Developers:
- **Template**: Starting point for new MCP servers
- **Reference**: Minimal working example
- **Testing**: Validate MCP client implementations
- **Prototype**: Quick server for testing ideas

---

*Ultra Minimal MCP Server - Your gateway to understanding MCP! 🎯*
