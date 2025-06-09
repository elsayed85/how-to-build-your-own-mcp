from mcp.server.fastmcp import FastMCP
from typing import Dict, Optional
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve():
    # 1. Create a FastMCP server instance
    mcp = FastMCP(name="Images_Generator_MCP_Server")

    # 2. Define a tool that generates a random image URL
    @mcp.tool(
        name="generate_image_url",
        description="""
        Generate a random image URL from Lorem Picsum.
        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            options (Dict[str, str], optional): Additional options for the image. Defaults to {}.
            
        available options:
            - grayscale: 1 for grayscale, 0 for color
            - blur: 1-10 for blur level
            - random: 1 for random image, 0 for specific image
            - seed: seed value for random image
            - quality: quality of the image (0-100)
        """,
    )
    async def generate_image_url(
        width: int, height: int, options: Optional[Dict[str, str]] = {}
    ) -> str:
        """
        Generate a random image URL from Lorem Picsum.
        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            options (Dict[str, str], optional): Additional options for the image. Defaults to {}.
        """

        url = f"https://picsum.photos/{width}/{height}"

        if options:
            url += "?" + "&".join(f"{key}={value}" for key, value in options.items())

        return url
    
    return mcp


def main():
    async def _run():
        server = await serve()
        logger.info("Starting Calculator MCP server...")
        return server

    server = asyncio.run(_run())
    server.run()  # This should work with stdio



if __name__ == "__main__":
    main()
