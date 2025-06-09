from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import asyncio
import logging
import httpx
import click


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def serve(auth_token: str):
    # 1. Create a FastMCP server instance
    mcp = FastMCP(name="DEV_TO_Blog_MCP_Server")

    # Base URL for dev.to API
    DEV_TO_BASE_URL = "https://dev.to/api"

    @mcp.tool(
        name="search_articles",
        description="""
        Search for articles on dev.to by topic/keyword.
        
        Args:
            query (str): The search query/topic to search for (e.g., "laravel authentication", "react hooks")
            per_page (int, optional): Number of articles to return per page (default: 10, max: 1000)
            page (int, optional): Page number for pagination (default: 1)
            tag (str, optional): Filter by specific tag
            username (str, optional): Filter by specific username
            state (str, optional): Filter by article state ("fresh" for recent articles)
            top (int, optional): Filter by top articles (7 for weekly, 30 for monthly, etc.)
        
        Returns:
            List of article objects with basic information including title, description, URL, tags, etc.
        """,
    )
    async def search_articles(
        query: str,
        per_page: Optional[int] = 10,
        page: Optional[int] = 1,
        tag: Optional[str] = None,
        username: Optional[str] = None,
        state: Optional[str] = None,
        top: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for articles on dev.to using the public API.
        """
        try:
            # Build query parameters
            params = {
                "per_page": min(per_page, 1000),  # API limit
                "page": page,
            }

            # Add search query if provided
            if query:
                # Replace spaces with + for better search results
                formatted_query = query.replace(" ", "+")
                params["q"] = formatted_query

            # Add optional filters
            if tag:
                params["tag"] = tag
            if username:
                params["username"] = username
            if state:
                params["state"] = state
            if top:
                params["top"] = top

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{DEV_TO_BASE_URL}/articles", params=params
                )
                response.raise_for_status()

                articles = response.json()

                # Return the articles
                return articles

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return {"error": f"Failed to fetch articles: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    @mcp.tool(
        name="get_article",
        description="""
        Get detailed information about a specific dev.to article by its ID or path.
        
        Args:
            article_id (str): The article ID or path (e.g., "2546060" or "devteam/join-the-worlds-largest-hackathon-1-million-in-prizes-3hfh")
        
        Returns:
            Detailed article object including full content (body_html, body_markdown), comments count, reactions, etc.
        """,
    )
    async def get_article(article_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific dev.to article.
        """
        try:
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{DEV_TO_BASE_URL}/articles/{article_id}")
                response.raise_for_status()

                article = response.json()

                return article

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 404:
                return {"error": f"Article with ID '{article_id}' not found"}
            return {"error": f"Failed to fetch article: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    @mcp.tool(
        name="get_tags",
        description="""
        Get popular tags from dev.to.
        
        Args:
            per_page (int, optional): Number of tags to return (default: 10, max: 1000)
            page (int, optional): Page number for pagination (default: 1)
        
        Returns:
            List of popular tags with their information
        """,
    )
    async def get_tags(
        per_page: Optional[int] = 10, page: Optional[int] = 1
    ) -> List[Dict[str, Any]]:
        """
        Get popular tags from dev.to.
        """
        try:
            params = {"per_page": min(per_page, 1000), "page": page}

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{DEV_TO_BASE_URL}/tags", params=params)
                response.raise_for_status()

                tags = response.json()

                return tags

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return {"error": f"Failed to fetch tags: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    @mcp.tool(
        name="create_article",
        description="""
        Create a new article on dev.to.
        
        Args:
            title (str): The title of the article
            body_markdown (str): The content of the article in markdown format
            published (bool, optional): Whether to publish the article immediately (default: False for draft)
            tags (List[str], optional): List of tags for the article (max 4 tags)
            description (str, optional): Brief description/summary of the article
            canonical_url (str, optional): Canonical URL if this is a cross-post
            main_image (str, optional): URL of the main image for the article
            organization_id (int, optional): ID of organization to publish under
            series (str, optional): Name of the series this article belongs to
        
        Returns:
            Created article object with details including ID, URL, etc.
            
        Note:
            - Requires a valid dev.to API key
            - Rate limited: if you hit the limit, wait 30 seconds before retrying
            - Articles are created as drafts by default (published=False)
        """,
    )
    async def create_article(
        title: str,
        body_markdown: str,
        published: Optional[bool] = False,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        canonical_url: Optional[str] = None,
        main_image: Optional[str] = None,
        organization_id: Optional[int] = None,
        series: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new article on dev.to using the API.
        """
        try:
            # Validate required fields
            if not title or not title.strip():
                return {"error": "Title is required and cannot be empty"}
            
            if not body_markdown or not body_markdown.strip():
                return {"error": "Body content (body_markdown) is required and cannot be empty"}

            # Prepare the article data
            article_data = {
                "title": title.strip(),
                "body_markdown": body_markdown,
                "published": published,
            }

            # Add optional fields if provided
            if tags:
                # Limit to max 4 tags as per dev.to requirements
                article_data["tags"] = tags[:4]
            
            if description:
                article_data["description"] = description
            
            if canonical_url:
                article_data["canonical_url"] = canonical_url
            
            if main_image:
                article_data["main_image"] = main_image
            
            if organization_id:
                article_data["organization_id"] = organization_id
            
            if series:
                article_data["series"] = series

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "api-key": auth_token,
            }
            

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DEV_TO_BASE_URL}/articles",
                    json={"article": article_data},
                    headers=headers,
                )
                response.raise_for_status()

                article = response.json()
                
                logger.info(f"Article created successfully: {article.get('title', 'Unknown title')}")
                return article

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    
                    status_code = e.response.status_code
                    
                    # Handle specific error cases based on dev.to API responses
                    if status_code == 400:
                        return {"error": "Bad request - Invalid article data provided", "details": error_detail}
                    elif status_code == 401:
                        return {"error": "Unauthorized - Invalid or missing API key", "details": error_detail}
                    elif status_code == 422:
                        error_msg = error_detail.get('error', 'Validation error')
                        return {"error": f"Validation error: {error_msg}", "details": error_detail}
                    elif status_code == 429:
                        return {"error": "Rate limit reached - Please try again in 30 seconds", "details": error_detail}
                    else:
                        return {"error": f"Failed to create article (HTTP {status_code})", "details": error_detail}
                except Exception:
                    return {"error": f"Failed to create article: HTTP {e.response.status_code}"}
            return {"error": f"Failed to create article: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    @mcp.tool(
        name="update_article",
        description="""
        Update an existing article on dev.to.
        
        Args:
            article_id (str): The ID of the article to update (e.g., "2546060")
            title (str, optional): The new title of the article
            body_markdown (str, optional): The new content of the article in markdown format
            published (bool, optional): Whether to publish/unpublish the article
            tags (List[str], optional): New list of tags for the article (max 4 tags)
            description (str, optional): New brief description/summary of the article
            canonical_url (str, optional): New canonical URL if this is a cross-post
            main_image (str, optional): New URL of the main image for the article
            organization_id (int, optional): ID of organization to publish under
            series (str, optional): Name of the series this article belongs to (use null to remove from series)
        
        Returns:
            Updated article object with details including ID, URL, etc.
            
        Note:
            - Requires a valid dev.to API key
            - Rate limited: if you hit the limit, wait 30 seconds before retrying
            - You can only update your own articles
            - If body_markdown contains front matter, it will take precedence over equivalent params
        """,
    )
    async def update_article(
        article_id: str,
        title: Optional[str] = None,
        body_markdown: Optional[str] = None,
        published: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        canonical_url: Optional[str] = None,
        main_image: Optional[str] = None,
        organization_id: Optional[int] = None,
        series: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing article on dev.to using the API.
        """
        try:
            # Validate article ID
            if not article_id or not article_id.strip():
                return {"error": "Article ID is required and cannot be empty"}

            # Prepare the article data with only provided fields
            article_data = {}

            if title is not None:
                if not title.strip():
                    return {"error": "Title cannot be empty if provided"}
                article_data["title"] = title.strip()
            
            if body_markdown is not None:
                if not body_markdown.strip():
                    return {"error": "Body content (body_markdown) cannot be empty if provided"}
                article_data["body_markdown"] = body_markdown
            
            if published is not None:
                article_data["published"] = published

            if tags is not None:
                # Limit to max 4 tags as per dev.to requirements
                article_data["tags"] = tags[:4]
            
            if description is not None:
                article_data["description"] = description
            
            if canonical_url is not None:
                article_data["canonical_url"] = canonical_url
            
            if main_image is not None:
                article_data["main_image"] = main_image
            
            if organization_id is not None:
                article_data["organization_id"] = organization_id
            
            if series is not None:
                article_data["series"] = series

            # Check if we have at least one field to update
            if not article_data:
                return {"error": "At least one field must be provided to update the article"}

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "api-key": auth_token,
            }

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{DEV_TO_BASE_URL}/articles/{article_id.strip()}",
                    json={"article": article_data},
                    headers=headers,
                )
                response.raise_for_status()

                article = response.json()
                
                logger.info(f"Article updated successfully: {article.get('title', 'Unknown title')}")
                return article

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    
                    status_code = e.response.status_code
                    
                    # Handle specific error cases based on dev.to API responses
                    if status_code == 400:
                        return {"error": "Bad request - Invalid article data provided", "details": error_detail}
                    elif status_code == 401:
                        return {"error": "Unauthorized - Invalid or missing API key", "details": error_detail}
                    elif status_code == 403:
                        return {"error": "Forbidden - You don't have permission to update this article", "details": error_detail}
                    elif status_code == 404:
                        return {"error": f"Article with ID '{article_id}' not found", "details": error_detail}
                    elif status_code == 422:
                        error_msg = error_detail.get('error', 'Validation error')
                        return {"error": f"Validation error: {error_msg}", "details": error_detail}
                    elif status_code == 429:
                        return {"error": "Rate limit reached - Please try again in 30 seconds", "details": error_detail}
                    else:
                        return {"error": f"Failed to update article (HTTP {status_code})", "details": error_detail}
                except Exception:
                    return {"error": f"Failed to update article: HTTP {e.response.status_code}"}
            return {"error": f"Failed to update article: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}

    return mcp


@click.command()
@click.option(
    "--auth-token",
    envvar="DEV_TO_AUTH_TOKEN",
    required=True,
    help="Dev.to authentication token",
)
def main(auth_token: str):
    async def _run():
        server = await serve(auth_token)
        logger.info("Starting DevTo Blog MCP server...")
        logger.info(f"Using auth token: {auth_token}")
        return server

    server = asyncio.run(_run())
    server.run()


if __name__ == "__main__":
    main()





