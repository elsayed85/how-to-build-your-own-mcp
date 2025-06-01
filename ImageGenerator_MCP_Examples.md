# 🖼️ Image Generator MCP Server - Practical Examples

## Overview
This document provides real-world prompt examples for using the Image Generator MCP Server, demonstrating various Lorem Picsum image generation scenarios.

---

## 📱 App Development Mockups

### Example 1: Social Media App Placeholders
```
I'm building a social media app and need placeholder images for the user interface:
- Profile pictures: 150x150 pixels
- Post images: 400x300 pixels  
- Story thumbnails: 100x100 pixels

Generate these placeholder images for my app mockup.
```

**Expected MCP Tool Calls:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "generate_image_url",
    "arguments": {
      "width": 150,
      "height": 150,
      "options": {"seed": "profile1"}
    }
  }
}
```

**Generated URLs:**
- Profile: `https://picsum.photos/150/150?seed=profile1`
- Post: `https://picsum.photos/400/300?seed=post1`
- Story: `https://picsum.photos/100/100?seed=story1`

---

### Example 2: E-commerce Product Grid
```
Create placeholder images for an e-commerce website:
- Product thumbnails: 250x250 (square format)
- Product details: 500x400 (landscape)
- Hero banner: 1200x400 (wide banner)

Make the thumbnails grayscale and add slight blur to the hero banner.
```

**Image Grid Layout:**
```mermaid
graph TD
    A[E-commerce Layout] --> B[Hero Banner<br/>1200x400 blur]
    A --> C[Product Grid]
    
    C --> D[Thumbnail 1<br/>250x250 grayscale]
    C --> E[Thumbnail 2<br/>250x250 grayscale]  
    C --> F[Thumbnail 3<br/>250x250 grayscale]
    
    D --> G[Detail View<br/>500x400 color]
    
    classDef banner fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef thumb fill:#9E9E9E,stroke:#424242,stroke-width:2px,color:#fff
    classDef detail fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    
    class B banner
    class D,E,F thumb
    class G detail
```

**MCP Tool Calls:**
1. Hero: `generate_image_url(1200, 400, {"blur": "2"})`
2. Thumbs: `generate_image_url(250, 250, {"grayscale": "1", "seed": "product1"})`
3. Detail: `generate_image_url(500, 400, {"seed": "product1"})`

---

## 🎨 Design & Creative Projects

### Example 3: Blog Post Headers
```
I'm writing a travel blog and need header images for different articles:
- "Mountain Adventures": 800x300 landscape
- "City Guides": 800x300 urban feel
- "Food Tours": 800x300 appetizing

Each should have a different aesthetic and be optimized for web.
```

**Blog Header Collection:**
```mermaid
graph LR
    A[Travel Blog] --> B[Mountain Adventures<br/>800x300]
    A --> C[City Guides<br/>800x300]
    A --> D[Food Tours<br/>800x300]
    
    B --> E[Nature Seed<br/>High Quality]
    C --> F[Urban Seed<br/>High Contrast]  
    D --> G[Warm Seed<br/>Food Colors]
    
    classDef blog fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef mountain fill:#8BC34A,stroke:#558B2F,stroke-width:2px,color:#fff
    classDef city fill:#607D8B,stroke:#37474F,stroke-width:2px,color:#fff
    classDef food fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A blog
    class B,E mountain
    class C,F city
    class D,G food
```

**MCP Tool Sequence:**
1. `generate_image_url(800, 300, {"seed": "mountain", "quality": "90"})`
2. `generate_image_url(800, 300, {"seed": "city", "quality": "90"})`
3. `generate_image_url(800, 300, {"seed": "food", "quality": "90"})`

---

### Example 4: Print Design Templates
```
I need background images for print materials:
- Business cards: 350x200 (subtle, professional)
- Flyers: 600x800 (eye-catching, vibrant)
- Letterhead: 600x150 (minimal, elegant)

The business cards should be grayscale, flyers should be colorful, letterhead should be high quality.
```

**Print Material Specifications:**
```mermaid
graph TD
    A[Print Design Suite] --> B[Business Cards]
    A --> C[Flyers]
    A --> D[Letterhead]
    
    B --> E[350x200<br/>Grayscale<br/>Professional]
    C --> F[600x800<br/>Colorful<br/>Eye-catching]
    D --> G[600x150<br/>High Quality<br/>Minimal]
    
    E --> H[seed: 'business'<br/>grayscale: 1]
    F --> I[seed: 'vibrant'<br/>random: 1]
    G --> J[seed: 'elegant'<br/>quality: 95]
    
    classDef print fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef business fill:#616161,stroke:#424242,stroke-width:2px,color:#fff
    classDef flyer fill:#f44336,stroke:#c62828,stroke-width:2px,color:#fff
    classDef letter fill:#3F51B5,stroke:#283593,stroke-width:2px,color:#fff
    
    class A print
    class B,E,H business
    class C,F,I flyer
    class D,G,J letter
```

**MCP Tool Calls:**
1. Cards: `generate_image_url(350, 200, {"grayscale": "1", "seed": "business"})`
2. Flyers: `generate_image_url(600, 800, {"random": "1", "seed": "vibrant"})`
3. Header: `generate_image_url(600, 150, {"quality": "95", "seed": "elegant"})`

---

## 🌐 Web Development

### Example 5: Responsive Image Sets
```
I need placeholder images for a responsive website:
- Mobile: 320x240
- Tablet: 768x576  
- Desktop: 1200x900
- Retina: 2400x1800

All should use the same seed for consistency but different sizes.
```

**Responsive Breakpoints:**
```mermaid
graph LR
    A[Same Image Content] --> B[Mobile<br/>320x240]
    A --> C[Tablet<br/>768x576]
    A --> D[Desktop<br/>1200x900]
    A --> E[Retina<br/>2400x1800]
    
    subgraph "Consistent Seed"
        F[seed: 'responsive']
        G[Same visual content]
        H[Different dimensions]
    end
    
    B --> F
    C --> F
    D --> F
    E --> F
    
    classDef device fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef config fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    
    class A,B,C,D,E device
    class F,G,H config
```

**MCP Tool Sequence:**
1. `generate_image_url(320, 240, {"seed": "responsive"})`
2. `generate_image_url(768, 576, {"seed": "responsive"})`
3. `generate_image_url(1200, 900, {"seed": "responsive"})`
4. `generate_image_url(2400, 1800, {"seed": "responsive"})`

---

### Example 6: Loading States & Placeholders
```
Create loading placeholder images for a photo gallery:
- Gallery grid: 300x300 squares
- Detail view: 600x400 landscape
- Thumbnails: 100x100 small squares

Use blur effect to simulate loading state, with different blur levels.
```

**Loading State Progression:**
```mermaid
graph TD
    A[Gallery Loading States] --> B[Heavy Blur<br/>Level 10]
    B --> C[Medium Blur<br/>Level 5]
    C --> D[Light Blur<br/>Level 2]
    D --> E[Sharp Image<br/>No Blur]
    
    A --> F[Thumbnail: 100x100]
    A --> G[Grid: 300x300]
    A --> H[Detail: 600x400]
    
    classDef loading fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef blur fill:#9E9E9E,stroke:#424242,stroke-width:2px,color:#fff
    classDef size fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    
    class A loading
    class B,C,D,E blur
    class F,G,H size
```

**MCP Blur Progression:**
1. `generate_image_url(300, 300, {"blur": "10", "seed": "gallery"})`
2. `generate_image_url(300, 300, {"blur": "5", "seed": "gallery"})`
3. `generate_image_url(300, 300, {"blur": "2", "seed": "gallery"})`
4. `generate_image_url(300, 300, {"seed": "gallery"})`

---

## 📖 Content Creation

### Example 7: Educational Materials
```
I'm creating an online course and need placeholder images:
- Course thumbnails: 400x225 (16:9 aspect ratio)
- Lesson previews: 300x200 (3:2 aspect ratio)  
- Assignment headers: 800x200 (4:1 banner)

Make thumbnails colorful, previews grayscale, and headers high quality.
```

**Educational Content Layout:**
```mermaid
graph TD
    A[Online Course Platform] --> B[Course Catalog]
    A --> C[Individual Course]
    A --> D[Assignment Section]
    
    B --> E[Thumbnail 1<br/>400x225 colorful]
    B --> F[Thumbnail 2<br/>400x225 colorful]
    
    C --> G[Lesson 1<br/>300x200 grayscale]
    C --> H[Lesson 2<br/>300x200 grayscale]
    
    D --> I[Assignment Banner<br/>800x200 high-quality]
    
    classDef platform fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef thumbnail fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef lesson fill:#616161,stroke:#424242,stroke-width:2px,color:#fff
    classDef assignment fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A,B,C,D platform
    class E,F thumbnail
    class G,H lesson
    class I assignment
```

**MCP Tool Calls:**
1. Thumbnails: `generate_image_url(400, 225, {"seed": "course1", "random": "1"})`
2. Lessons: `generate_image_url(300, 200, {"grayscale": "1", "seed": "lesson1"})`
3. Assignments: `generate_image_url(800, 200, {"quality": "95", "seed": "assignment"})`

---

## 🎪 Event & Marketing

### Example 8: Social Media Campaign
```
Create a series of images for a product launch campaign:
- Instagram posts: 1080x1080 (square)
- Instagram stories: 1080x1920 (vertical)
- Facebook covers: 820x312 (wide banner)
- Twitter headers: 1500x500 (3:1 ratio)

All should maintain visual consistency with the same seed but optimized for each platform.
```

**Social Media Asset Grid:**
```mermaid
graph LR
    A[Product Launch Campaign] --> B[Instagram]
    A --> C[Facebook]  
    A --> D[Twitter]
    
    B --> E[Posts<br/>1080x1080]
    B --> F[Stories<br/>1080x1920]
    
    C --> G[Cover<br/>820x312]
    
    D --> H[Header<br/>1500x500]
    
    subgraph "Consistent Branding"
        I[seed: 'product-launch']
        J[High Quality: 90+]
        K[Same Visual Theme]
    end
    
    E --> I
    F --> I
    G --> I
    H --> I
    
    classDef campaign fill:#E91E63,stroke:#AD1457,stroke-width:2px,color:#fff
    classDef instagram fill:#E1306C,stroke:#C13584,stroke-width:2px,color:#fff
    classDef facebook fill:#1877F2,stroke:#166FE5,stroke-width:2px,color:#fff
    classDef twitter fill:#1DA1F2,stroke:#0D8BD9,stroke-width:2px,color:#fff
    classDef brand fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    
    class A campaign
    class B,E,F instagram
    class C,G facebook
    class D,H twitter
    class I,J,K brand
```

**Campaign Asset Generation:**
1. IG Post: `generate_image_url(1080, 1080, {"seed": "product-launch", "quality": "90"})`
2. IG Story: `generate_image_url(1080, 1920, {"seed": "product-launch", "quality": "90"})`
3. FB Cover: `generate_image_url(820, 312, {"seed": "product-launch", "quality": "90"})`
4. Twitter: `generate_image_url(1500, 500, {"seed": "product-launch", "quality": "90"})`

---

## 🖼️ Advanced Image Techniques

### Example 9: A/B Testing Variants
```
I need to test different image styles for my landing page hero:
- Version A: Sharp, colorful image (1200x600)
- Version B: Subtle blur, muted colors (1200x600)  
- Version C: Grayscale, high contrast (1200x600)

All should use different seeds but same dimensions for fair comparison.
```

**A/B Testing Setup:**
```mermaid
graph TD
    A[Landing Page A/B Test] --> B[Version A<br/>Sharp & Colorful]
    A --> C[Version B<br/>Blur & Muted]
    A --> D[Version C<br/>Grayscale]
    
    B --> E[seed: 'variant-a'<br/>quality: 95]
    C --> F[seed: 'variant-b'<br/>blur: 3]
    D --> G[seed: 'variant-c'<br/>grayscale: 1]
    
    E --> H[Conversion Rate A]
    F --> I[Conversion Rate B]
    G --> J[Conversion Rate C]
    
    H --> K[Best Performer]
    I --> K
    J --> K
    
    classDef test fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    classDef variant fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef metric fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    classDef result fill:#f44336,stroke:#c62828,stroke-width:2px,color:#fff
    
    class A test
    class B,C,D,E,F,G variant
    class H,I,J metric
    class K result
```

**A/B Test Image Generation:**
1. Version A: `generate_image_url(1200, 600, {"seed": "variant-a", "quality": "95"})`
2. Version B: `generate_image_url(1200, 600, {"seed": "variant-b", "blur": "3"})`
3. Version C: `generate_image_url(1200, 600, {"seed": "variant-c", "grayscale": "1"})`

---

### Example 10: Progressive Image Loading
```
Implement progressive loading for a photography portfolio:
- Start with 50x50 heavily blurred thumbnail
- Progress to 200x200 medium blur
- Load 400x400 light blur  
- Finally show 800x800 sharp image

Use same seed throughout for consistency.
```

**Progressive Loading Sequence:**
```mermaid
graph LR
    A[Image Loading] --> B[Step 1<br/>50x50 blur:10]
    B --> C[Step 2<br/>200x200 blur:5]
    C --> D[Step 3<br/>400x400 blur:2]
    D --> E[Step 4<br/>800x800 sharp]
    
    F[Same Seed: 'portfolio'] --> B
    F --> C
    F --> D
    F --> E
    
    classDef loading fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef step fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef seed fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A loading
    class B,C,D,E step
    class F seed
```

**Progressive Load Calls:**
1. `generate_image_url(50, 50, {"seed": "portfolio", "blur": "10"})`
2. `generate_image_url(200, 200, {"seed": "portfolio", "blur": "5"})`
3. `generate_image_url(400, 400, {"seed": "portfolio", "blur": "2"})`
4. `generate_image_url(800, 800, {"seed": "portfolio"})`

---

## 🔧 Image Generator Features

```mermaid
graph TD
    subgraph "Core Functionality"
        A[generate_image_url] --> B[Width & Height<br/>Required parameters]
        B --> C[Options Object<br/>Optional enhancements]
    end
    
    subgraph "Available Options"
        D[grayscale: 0-1] --> E[Color/Monochrome]
        F[blur: 1-10] --> G[Blur intensity]
        H[random: 0-1] --> I[Random/Specific]
        J[seed: string] --> K[Consistent images]
        L[quality: 0-100] --> M[JPEG quality]
    end
    
    subgraph "Use Cases"
        N[Mockups] --> O[App development]
        P[Placeholders] --> Q[Web design]
        R[Testing] --> S[A/B variants]
        T[Loading] --> U[Progressive states]
    end
    
    classDef core fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    classDef option fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    classDef usecase fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    class A,B,C core
    class D,F,H,J,L,E,G,I,K,M option
    class N,P,R,T,O,Q,S,U usecase
```

---

## 🚀 Quick Testing Commands

```bash
# Test the image generator server
cd /Users/elsayed/side-projects/sessions/stdio_mcp_server

# Start the image generator server
uv run python image_generator_mcp_server.py

# In another terminal, test with MCP client
cd ../mcp_client
uv run python client.py ../stdio_mcp_server/image_generator_mcp_server.py

# Example client commands:
# generate_image_url 400 300
# generate_image_url 800 600 '{"grayscale": "1"}'
# generate_image_url 1200 800 '{"blur": "3", "seed": "test"}'
# generate_image_url 300 300 '{"quality": "95", "random": "1"}'
```

---

## 💡 Pro Tips

### Best Practices:
- **Consistent Seeds**: Use same seed for related images
- **Quality Settings**: Use 90+ for final production images  
- **Progressive Loading**: Start blurred, progress to sharp
- **A/B Testing**: Use different seeds for fair comparison
- **Responsive Design**: Generate multiple sizes with same seed

### Common Patterns:
- **Hero Images**: 1200x600 with high quality
- **Thumbnails**: 300x300 or smaller, can use grayscale
- **Social Media**: Platform-specific dimensions
- **Loading States**: Multiple blur levels with same seed
- **Print Materials**: Higher quality settings (95+)

---

*Image Generator MCP Server - Beautiful placeholders for every project! 🖼️*
