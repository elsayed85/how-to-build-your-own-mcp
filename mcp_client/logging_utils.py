"""
Logging utilities for the MCP Langchain client.
Provides structured logging with custom formatting and separation between queries.
"""

import os
import logging
from datetime import datetime
from typing import List, Any


class CustomFormatter(logging.Formatter):
    """Custom formatter for clear, structured logs with timestamps."""
    
    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return f"[{timestamp}] [{record.levelname:8}] {record.getMessage()}"


class MCPLogger:
    """Centralized logging manager for MCP client operations."""
    
    def __init__(self, name: str = "langchain_mcp_client", log_dir: str = None):
        """Initialize the logger with file and console handlers."""
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), "logs")
        
        os.makedirs(log_dir, exist_ok=True)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(os.path.join(log_dir, "langchain_client.log"))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(CustomFormatter())
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(CustomFormatter())
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_startup(self):
        """Log application startup."""
        self.logger.info("=" * 80)
        self.logger.info("STARTING LANGCHAIN MCP CLIENT")
        self.logger.info("=" * 80)
    
    def log_completion(self):
        """Log application completion."""
        self.logger.info("=" * 80)
        self.logger.info("LANGCHAIN MCP CLIENT COMPLETED SUCCESSFULLY")
        self.logger.info("=" * 80)
    
    def log_step(self, step_number: int, description: str):
        """Log a step in the process."""
        self.logger.info("-" * 40)
        self.logger.info(f"STEP {step_number}: {description}")
    
    def log_success(self, message: str):
        """Log a successful operation."""
        self.logger.info(f"✓ {message}")
    
    def log_error(self, message: str, exception: Exception = None):
        """Log an error with optional exception details."""
        self.logger.error(f"✗ {message}")
        if exception:
            self.logger.error(f"Error type: {type(exception)}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def log_info(self, message: str):
        """Log general information."""
        self.logger.info(message)
    
    def log_query_start(self, query_number: int, query: str, history_length: int):
        """Log the start of a new query with separation."""
        self.logger.info("=" * 60)
        self.logger.info("=" * 60)
        self.logger.info("=" * 60)
        self.logger.info(f"🔍 QUERY #{query_number}: Executing user query...")
        self.logger.info(f"Query: {query}")
        self.logger.info(f"Conversation history length: {history_length} messages")
    
    def log_query_success(self, updated_history_length: int):
        """Log successful query execution."""
        self.logger.info("✓ Query executed successfully")
        self.logger.info(f"Updated conversation history to {updated_history_length} messages")
    
    def log_response_analysis(self, query_number: int, response_type: str, message_count: int):
        """Log response analysis details."""
        self.logger.info("-" * 60)
        self.logger.info(f"📊 RESPONSE ANALYSIS #{query_number}:")
        self.logger.info(f"Response type: {response_type}")
        self.logger.info(f"Total messages in conversation: {message_count}")
    
    def log_conversation_flow_header(self):
        """Log conversation flow section header."""
        self.logger.info("\n" + "=" * 50)
        self.logger.info("CONVERSATION FLOW:")
        self.logger.info("=" * 50)
    
    def log_message_details(self, index: int, message_type: str, content: str = None, 
                           tool_calls: List[dict] = None, tool_name: str = None, 
                           tool_result: str = None):
        """Log details of a specific message in the conversation."""
        self.logger.info(f"\n{index}. {message_type}:")
        
        if content:
            self.logger.info(f"   Content: {content}")
        
        if tool_calls:
            self.logger.info("   Tool Calls:")
            for tool_call in tool_calls:
                self.logger.info(f"     - {tool_call['name']}({tool_call['args']})")
        
        if tool_name:
            self.logger.info(f"   Tool: {tool_name}")
            if tool_result:
                self.logger.info(f"   Result: {tool_result}")
    
    def log_final_answer(self, query_number: int, answer: str):
        """Log the final answer for a query."""
        self.logger.info("\n" + "=" * 50)
        self.logger.info(f"FINAL ANSWER #{query_number}:")
        self.logger.info("=" * 50)
        self.logger.info(f"{answer}")
        self.logger.info("=" * 50)
    
    def log_query_separation(self):
        """Add visual separation between queries."""
        self.logger.info("=" * 80)
        self.logger.info("=" * 80)
        self.logger.info("=" * 80)
    
    def log_chat_session_end(self, reason: str = "user"):
        """Log chat session end."""
        if reason == "user":
            self.logger.info("Chat session ended by user")
        elif reason == "interrupt":
            self.logger.info("Chat session interrupted by user")
        else:
            self.logger.info(f"Chat session ended: {reason}")
    
    def log_chat_error(self, error_message: str):
        """Log errors that occur during chat loop."""
        self.logger.error(f"Error in chat loop: {error_message}")


def create_logger(name: str = "langchain_mcp_client", log_dir: str = None) -> MCPLogger:
    """Factory function to create a configured MCP logger."""
    return MCPLogger(name, log_dir)
