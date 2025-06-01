# 🎨 Image Generator MCP Server Architecture

## Overview
The Image Generator MCP Server provides dynamic image URL generation using Lorem Picsum service through a simple MCP interface.

---

## 🏗️ Server Architecture

```mermaid
graph TB
    subgraph "Image Generator MCP Server"
        direction TB
        A[FastMCP Server<br/>Images_Generator_MCP_Server] --> B[Tool Registry]
        
        B --> C[generate_image_url]
        
        C --> D[URL Builder Engine]
        D --> E[Base URL Constructor<br/>picsum.photos/width/height]
        D --> F[Options Processor<br/>Query Parameters]
        
        F --> G[Grayscale Option]
        F --> H[Blur Effect Option] 
        F --> I[Random Seed Option]
        F --> J[Quality Option]
    end
    
    subgraph "External Service"
        K[Lorem Picsum API<br/>https://picsum.photos] --> L[Random Image Database<br/>High Quality Photos]
    end
    
    D --> K
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    classDef tool fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef engine fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef options fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef external fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    
    class A server
    class C tool
    class D,E,F engine
    class G,H,I,J options
    class K,L external
```

---

## 🎛️ Image Customization Options

```mermaid
graph LR
    subgraph "Core Parameters"
        A1[Width] --> A2[Image width in pixels<br/>Required parameter]
        B1[Height] --> B2[Image height in pixels<br/>Required parameter]
    end
    
    subgraph "Visual Effects"
        C1[Grayscale] --> C2[0: Color image<br/>1: Black & white]
        D1[Blur] --> D2[1-10: Blur intensity<br/>Higher = more blur]
    end
    
    subgraph "Randomization"
        E1[Random] --> E2[0: Specific image<br/>1: Random selection]
        F1[Seed] --> F2[Custom seed value<br/>Reproducible randomness]
    end
    
    subgraph "Quality Control"
        G1[Quality] --> G2[0-100: JPEG quality<br/>Higher = better quality]
    end
    
    classDef core fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef effects fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff  
    classDef random fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef quality fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A1,A2,B1,B2 core
    class C1,C2,D1,D2 effects
    class E1,E2,F1,F2 random
    class G1,G2 quality
```

---

## 🔧 URL Generation Process

```mermaid
graph TD
    A[Client Request] --> B[Extract Dimensions<br/>width × height]
    B --> C[Validate Parameters<br/>width > 0, height > 0]
    C --> D{Options Provided?}
    
    D -->|No| E[Generate Base URL<br/>https://picsum.photos/width/height]
    D -->|Yes| F[Process Options Dictionary]
    
    F --> G[Build Query String<br/>key=value&key=value]
    G --> H[Combine Base URL + Query<br/>https://picsum.photos/800/600?grayscale=1&blur=5]
    
    E --> I[Return Simple URL]
    H --> I
    
    I --> J[Client Receives Image URL<br/>Ready for use in applications]
    
    classDef process fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef decision fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef result fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    
    class A,B,C,F,G,H process
    class D decision
    class E,I,J result
```

---

## 🌐 Lorem Picsum Integration

```mermaid
graph LR
    subgraph "MCP Server"
        A[generate_image_url Tool] --> B[URL Constructor]
    end
    
    subgraph "Lorem Picsum Service"
        C[Image Database] --> D[Random Photo Selection]
        D --> E[Image Processing Pipeline]
        E --> F[Apply Effects<br/>Grayscale, Blur, Quality]
        F --> G[Serve Processed Image]
    end
    
    B -->|HTTP GET Request| C
    G -->|Image Response| H[Client Application]
    
    subgraph "Image Formats"
        I[JPEG - Default format]
        J[Custom dimensions]
        K[Real photographs]
        L[High resolution available]
    end
    
    G --> I
    G --> J
    G --> K
    G --> L
    
    classDef server fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef service fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef format fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef client fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    
    class A,B server
    class C,D,E,F,G service
    class I,J,K,L format
    class H client
```

---

## 🐳 Docker Deployment Flow

```mermaid
graph TD
    A[Image Generator Source] --> B[Docker Build]
    B --> C[Python 3.12 Slim Base]
    C --> D[Install UV Package Manager<br/>Lightweight dependency management]
    D --> E[Install Project Dependencies<br/>FastMCP, typing extensions]
    E --> F[Copy Server Script<br/>image_generator_mcp_server.py]
    F --> G[Configure Virtual Environment<br/>Set PATH for .venv/bin]
    G --> H[Container Ready for Execution]
    
    H --> I[Docker Run Command]
    I --> J[Image Generator MCP Server<br/>Running on stdio transport]
    
    J --> K[Ready to Generate<br/>Custom Image URLs]
    
    classDef source fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef build fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    classDef ready fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    
    class A source
    class B,C,D,E,F,G build
    class H,I,J,K ready
```

---

## 🔄 Request/Response Examples

```mermaid
sequenceDiagram
    participant Client
    participant MCP Server
    participant Lorem Picsum
    
    Note over Client,Lorem Picsum: Simple Image Generation
    Client->>MCP Server: generate_image_url(800, 600)
    MCP Server->>MCP Server: Build URL: picsum.photos/800/600
    MCP Server->>Client: Return URL string
    Client->>Lorem Picsum: HTTP GET to URL
    Lorem Picsum->>Client: Return 800x600 image
    
    Note over Client,Lorem Picsum: Advanced Image with Effects
    Client->>MCP Server: generate_image_url(400, 300, {grayscale: 1, blur: 3})
    MCP Server->>MCP Server: Build URL: picsum.photos/400/300?grayscale=1&blur=3
    MCP Server->>Client: Return enhanced URL
    Client->>Lorem Picsum: HTTP GET to enhanced URL
    Lorem Picsum->>Client: Return processed image with effects
```

---

## 📋 Quick Commands

### Build & Run
```bash
# Build Docker image
docker build -f imageGeneratorMcp.Dockerfile -t image-generator-mcp .

# Run container
docker run -i --rm image-generator-mcp

# Direct Python execution
uv run python image_generator_mcp_server.py
```

### Tool Usage Examples
```json
{
  "name": "generate_image_url",
  "arguments": {
    "width": 800,
    "height": 600
  }
}
// Returns: "https://picsum.photos/800/600"

{
  "name": "generate_image_url",
  "arguments": {
    "width": 400,
    "height": 300,
    "options": {
      "grayscale": "1",
      "blur": "5",
      "random": "1"
    }
  }
}
// Returns: "https://picsum.photos/400/300?grayscale=1&blur=5&random=1"
```

---

## 🎯 Use Cases & Applications

```mermaid
mindmap
  root((Image Generator<br/>Use Cases))
    Web Development
      Placeholder images
      Mockup designs
      Template previews
      Loading states
    Content Creation
      Blog post images
      Social media content
      Presentation visuals
      Documentation assets
    Testing & Development
      Image loading tests
      UI component testing
      Performance testing
      Responsive design
    Design & Prototyping
      Wireframe placeholders
      Design system examples
      Color scheme testing
      Layout validation
```

---

## 🎯 Key Features

- 🖼️ **Dynamic Image URLs**: Generate custom-sized image URLs instantly
- 🎨 **Visual Effects**: Grayscale, blur, and quality control options
- 🎲 **Randomization**: Random images with optional seed control
- 📐 **Custom Dimensions**: Any width and height combination
- 🚀 **Lightning Fast**: URL generation without image processing delays
- 🌐 **External Integration**: Leverages Lorem Picsum's robust image service
- 🐳 **Container Ready**: Docker deployment for easy scaling
- 💡 **Simple Interface**: Single tool with comprehensive options
- 🔧 **Developer Friendly**: Perfect for prototyping and testing
- 📱 **Responsive Ready**: Generate images for different screen sizes

---

## 🌟 Advanced Examples

```javascript
// Web development placeholder
generate_image_url(1200, 400, {quality: "90"})
// Perfect for hero sections

// Social media content
generate_image_url(1080, 1080, {grayscale: "1"}) 
// Instagram-ready square images

// Blog thumbnails with effects
generate_image_url(600, 400, {blur: "2", seed: "blog-post-123"})
// Consistent blur effect for article headers
```

---

*Image Generator MCP Server - Beautiful placeholder images at your fingertips! 🎨*
