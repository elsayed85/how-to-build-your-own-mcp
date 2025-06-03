"""
Minimal MCP Client Example
A simplified version that demonstrates the core concept of using MCP with LangChain
without logging or interactive chat features.
"""

import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Configuration
mcp_dir = os.path.dirname(os.path.abspath(__file__)) + "/../stdio_mcp_server"
dev_blog_auth_token = os.getenv("DEV_BLOG_AUTH_TOKEN", "")

server_config = {
    "math": {
        "command": "python",
        "args": [f"{mcp_dir}/calculator_mcp_server.py"],
        "transport": "stdio",
    },
    "image-generation": {
        "command": "python",
        "args": [f"{mcp_dir}/image_generator_mcp_server.py"],
        "transport": "stdio",
    },
    "dev-blog": {
        "command": "python",
        "args": [
            f"{mcp_dir}/dev_blog_mcp_server.py",
            "--auth-token",
            dev_blog_auth_token,
        ],
        "transport": "stdio",
    },
}


async def ask_question(question: str) -> str:
    """
    Ask a question using MCP servers and return the answer.
    
    This function demonstrates the core workflow:
    1. Create MCP client
    2. Get available tools from servers
    3. Create LangChain agent with tools
    4. Execute the question
    5. Return the answer
    """
    
    # Step 1: Create MCP client
    client = MultiServerMCPClient(server_config)
    
    # Step 2: Get tools from MCP servers
    tools = await client.get_tools()
    
    # Step 3: Create LangChain agent with the tools
    agent = create_react_agent("gpt-4o-mini", tools)
    
    # Step 4: Execute the question
    response = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    
    # Step 5: Extract and return the final answer
    messages = response.get("messages", [])
    if messages:
        final_message = messages[-1]
        if hasattr(final_message, "content"):
            return final_message.content
    
    return "No response received"


async def main():
    """Main function to demonstrate the minimal MCP client."""
    
    # Example questions to demonstrate different MCP servers
    questions = [
        "What is 25 + 37?",
        "Calculate the square root of 144",
        "What is 15 * 8 + 20?",
    ]
    
    print("🤖 Minimal MCP Client Demo")
    print("=" * 40)
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        try:
            answer = await ask_question(question)
            print(f"💡 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Demo completed!")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())
