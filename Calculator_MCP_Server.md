# 🧮 Calculator MCP Server Architecture

## Overview
The Calculator MCP Server provides basic mathematical operations through a clean MCP interface.

---

## 🏗️ Server Architecture

```mermaid
graph TB
    subgraph "Calculator MCP Server" 
        direction TB
        A[FastMCP Server<br/>Calculator_MCP_Server] --> B[Tool Registry]
        
        B --> C[sum_two_numbers]
        B --> D[subtract_two_numbers] 
        B --> E[multiply_two_numbers]
        
        C --> F[Addition Logic<br/>a + b]
        D --> G[Subtraction Logic<br/>a - b]
        E --> H[Multiplication Logic<br/>a * b]
    end
    
    subgraph "Client Interface"
        I[MCP Client] -->|stdio/HTTP| A
    end
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef tool fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef logic fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef client fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A server
    class C,D,E tool
    class F,G,H logic
    class I client
```

---

## 🔧 Tool Details

```mermaid
graph LR
    subgraph "Available Tools"
        direction TB
        
        subgraph "Sum Tool"
            A1[sum_two_numbers] --> A2[Input: a, b<br/>Type: int]
            A2 --> A3[Output: String<br/>Result + message]
        end
        
        subgraph "Subtract Tool"
            B1[subtract_two_numbers] --> B2[Input: a, b<br/>Type: int]
            B2 --> B3[Output: String<br/>Result + message]
        end
        
        subgraph "Multiply Tool"
            C1[multiply_two_numbers] --> C2[Input: a, b<br/>Type: int]
            C2 --> C3[Output: String<br/>Result + message]
        end
    end
    
    classDef toolName fill:#2196F3,stroke:#1565C0,stroke-width:3px,color:#fff
    classDef input fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef output fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A1,B1,C1 toolName
    class A2,B2,C2 input
    class A3,B3,C3 output
```

---

## 🐳 Docker Deployment Flow

```mermaid
graph TD
    A[Source Code] --> B[Docker Build]
    B --> C[Python 3.12 Base Image]
    C --> D[Install UV Package Manager]
    D --> E[Install Dependencies<br/>pyproject.toml]
    E --> F[Copy Server Script]
    F --> G[Set Virtual Environment PATH]
    G --> H[Container Ready]
    
    H --> I[Docker Run]
    I --> J[Calculator MCP Server<br/>Running on stdio]
    
    classDef source fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef build fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    classDef ready fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    
    class A source
    class B,C,D,E,F,G build
    class H,I,J ready
```

---

## 🔄 Request/Response Flow

```mermaid
sequenceDiagram
    participant Client
    participant FastMCP
    participant Tool
    
    Client->>FastMCP: Initialize Connection
    FastMCP->>Client: Server Capabilities
    
    Client->>FastMCP: List Tools Request
    FastMCP->>Client: [sum, subtract, multiply]
    
    Client->>FastMCP: Call sum_two_numbers(5, 3)
    FastMCP->>Tool: Execute Addition
    Tool->>Tool: Calculate 5 + 3 = 8
    Tool->>FastMCP: Return "The sum of 5 and 3 is 8"
    FastMCP->>Client: Response with result
    
    Note over Client,Tool: Simple, fast mathematical operations
```

---

## 📋 Quick Commands

### Build & Run
```bash
# Build Docker image
docker build -f calculatorMcp.Dockerfile -t calculator-mcp .

# Run container
docker run -i --rm calculator-mcp

# Direct Python execution
uv run python calculator_mcp_server.py
```

### Tool Usage Examples
```json
{
  "name": "sum_two_numbers",
  "arguments": {"a": 10, "b": 5}
}
// Returns: "The sum of 10 and 5 is 15 (Calculated by MCP server)."

{
  "name": "multiply_two_numbers", 
  "arguments": {"a": 7, "b": 3}
}
// Returns: "The product of 7 and 3 is 21 (Calculated by MCP server)."
```

---

## 🎯 Key Features

- ✅ **Simple Math Operations**: Addition, subtraction, multiplication
- 🚀 **FastMCP Framework**: Quick setup and deployment
- 🐳 **Docker Ready**: Containerized for easy deployment
- 📡 **stdio Transport**: Standard input/output communication
- 🔒 **Type Safety**: Integer input validation
- 💬 **Descriptive Responses**: Clear result messages

---

*Calculator MCP Server - Making math simple through MCP! 🧮*
