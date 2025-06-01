# 📝 Dev Blog MCP Server Architecture

## Overview
The Dev Blog MCP Server provides comprehensive dev.to blog management capabilities through MCP interface with full CRUD operations.

---

## 🏗️ Server Architecture

```mermaid
graph TB
    subgraph "Dev Blog MCP Server"
        direction TB
        A[FastMCP Server<br/>DEV_TO_Blog_MCP_Server] --> B[Authentication Layer<br/>API Token]
        B --> C[Tool Registry]
        
        C --> D[search_articles]
        C --> E[get_article]
        C --> F[get_comments]
        C --> G[get_tags]
        C --> H[create_article]
        C --> I[update_article]
        
        D --> J[Dev.to Public API<br/>Search & Filter]
        E --> K[Dev.to Public API<br/>Article Details]
        F --> L[Dev.to Public API<br/>Comments Retrieval]
        G --> M[Dev.to Public API<br/>Tags Management]
        H --> N[Dev.to Authenticated API<br/>Article Creation]
        I --> O[Dev.to Authenticated API<br/>Article Updates]
    end
    
    subgraph "External Integration"
        P[dev.to API<br/>https://dev.to/api] --> Q[HTTP Client<br/>httpx AsyncClient]
    end
    
    Q --> J
    Q --> K
    Q --> L
    Q --> M
    Q --> N
    Q --> O
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef auth fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    classDef tool fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef api fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef external fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A server
    class B auth
    class D,E,F,G,H,I tool
    class J,K,L,M,N,O api
    class P,Q external
```

---

## 🔧 Tool Categories

```mermaid
graph TD
    subgraph "Read Operations (Public)"
        A1[search_articles] --> A2[🔍 Search by query/topic<br/>Filter by tags, username<br/>Pagination support]
        B1[get_article] --> B2[📄 Fetch article details<br/>Full content + metadata<br/>By ID or path]
        C1[get_comments] --> C2[💬 Get article comments<br/>Community engagement<br/>Comment threads]
        D1[get_tags] --> D2[🏷️ Popular tags list<br/>Trending topics<br/>Tag statistics]
    end
    
    subgraph "Write Operations (Authenticated)"
        E1[create_article] --> E2[✍️ Create new articles<br/>Markdown support<br/>Draft/Publish options]
        F1[update_article] --> F2[📝 Update existing articles<br/>Edit content/metadata<br/>Series management]
    end
    
    classDef read fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef write fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    classDef details fill:#2196F3,stroke:#1565C0,stroke-width:1px,color:#fff
    
    class A1,B1,C1,D1 read
    class E1,F1 write
    class A2,B2,C2,D2,E2,F2 details
```

---

## 🔐 Authentication & Security Flow

```mermaid
graph LR
    A[Client Request] --> B{Requires Auth?}
    B -->|No| C[Public API Call<br/>search, get, comments, tags]
    B -->|Yes| D[Check API Token]
    D --> E{Token Valid?}
    E -->|No| F[❌ Unauthorized Error<br/>401/403 Response]
    E -->|Yes| G[Authenticated API Call<br/>create, update articles]
    
    C --> H[✅ Public Data Response]
    G --> I[✅ Authenticated Response]
    
    classDef process fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef decision fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef success fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef error fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    
    class A,C,G process
    class B,E decision
    class H,I success
    class F error
```

---

## 🐳 Docker Deployment Architecture

```mermaid
graph TD
    A[Dev Blog Source] --> B[Docker Build Process]
    B --> C[Python 3.12 Base Image]
    C --> D[Install UV + Dependencies<br/>httpx, mcp, click]
    D --> E[Copy Server Script<br/>dev_blog_mcp_server.py]
    E --> F[Environment Setup<br/>Virtual Environment PATH]
    F --> G[Runtime Configuration<br/>Auth Token via ENV]
    
    G --> H[Container Ready]
    H --> I[Docker Run with Token]
    I --> J[Dev Blog MCP Server<br/>Connected to dev.to API]
    
    subgraph "Environment Variables"
        K[DEV_TO_AUTH_TOKEN<br/>Required for write operations]
    end
    
    K --> I
    
    classDef source fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef build fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    classDef ready fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef env fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A source
    class B,C,D,E,F,G build
    class H,I,J ready
    class K env
```

---

## 🔄 Article Creation Workflow

```mermaid
sequenceDiagram
    participant Client
    participant MCP Server
    participant Dev.to API
    participant Database
    
    Client->>MCP Server: create_article(title, content, tags)
    MCP Server->>MCP Server: Validate inputs & auth token
    MCP Server->>MCP Server: Prepare article payload
    
    Note over MCP Server: Max 4 tags, markdown content
    
    MCP Server->>Dev.to API: POST /articles with auth headers
    Dev.to API->>Database: Store article (draft/published)
    Database->>Dev.to API: Article created with ID
    Dev.to API->>MCP Server: Article response + URL
    MCP Server->>Client: Success with article details
    
    Note over Client,Database: Article now available on dev.to
```

---

## 📊 API Response Data Flow

```mermaid
graph LR
    subgraph "Search Articles Response"
        A1[Article List] --> A2[Title, Description, URL]
        A2 --> A3[Tags, Published Date]
        A3 --> A4[Author Info, Reactions]
    end
    
    subgraph "Get Article Response" 
        B1[Full Article] --> B2[Complete Markdown Content]
        B2 --> B3[HTML Content, Comments Count]
        B3 --> B4[Social Stats, Reading Time]
    end
    
    subgraph "Create/Update Response"
        C1[Operation Result] --> C2[Article ID, Public URL]
        C2 --> C3[Publication Status]
        C3 --> C4[Success/Error Messages]
    end
    
    classDef search fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef article fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef operation fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A1,A2,A3,A4 search
    class B1,B2,B3,B4 article
    class C1,C2,C3,C4 operation
```

---

## 📋 Quick Commands

### Build & Run
```bash
# Build Docker image
docker build -f devBlogMcp.Dockerfile -t dev-blog-mcp .

# Run with auth token
docker run -i --rm -e DEV_TO_AUTH_TOKEN=your_token dev-blog-mcp

# Direct Python execution
DEV_TO_AUTH_TOKEN=your_token uv run python dev_blog_mcp_server.py
```

### Tool Usage Examples
```json
{
  "name": "search_articles",
  "arguments": {
    "query": "react hooks",
    "per_page": 5,
    "tag": "javascript"
  }
}

{
  "name": "create_article",
  "arguments": {
    "title": "My Dev Article",
    "body_markdown": "# Hello World\nThis is my article content...",
    "published": false,
    "tags": ["tutorial", "beginners"]
  }
}
```

---

## 🎯 Key Features

- 🔍 **Advanced Search**: Query articles by topic, tags, username
- 📄 **Full Article Access**: Complete content and metadata retrieval
- ✍️ **Content Creation**: Create and publish articles with markdown
- 📝 **Content Management**: Update existing articles and metadata
- 💬 **Community Data**: Access comments and engagement metrics
- 🏷️ **Tag Management**: Discover and use popular tags
- 🔐 **Secure Operations**: Token-based authentication for write operations
- 📊 **Rich Responses**: Detailed article data and statistics
- 🚫 **Error Handling**: Comprehensive error reporting and rate limiting
- 🐳 **Docker Ready**: Containerized deployment with environment configuration

---

*Dev Blog MCP Server - Your gateway to dev.to content management! 📝*
