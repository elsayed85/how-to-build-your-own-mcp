#!/usr/bin/env python3
"""
Script to watch MCP payload logs in real-time.
Usage: python watch_payloads.py
"""

import sys
import time
import os

def watch_log_file(filename):
    """Watch a log file and print new lines as they appear."""
    try:
        with open(filename, 'r') as file:
            # Go to the end of the file
            file.seek(0, 2)
            
            print(f"Watching {filename} for new MCP payload logs...")
            print("=" * 80)
            
            while True:
                line = file.readline()
                if line:
                    print(line.rstrip())
                else:
                    time.sleep(0.1)
                    
    except FileNotFoundError:
        print(f"Log file {filename} not found. Make sure the MCP client is running.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopped watching log file.")
        sys.exit(0)

if __name__ == "__main__":
    log_file = "logs/mcp_payloads.log"
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create empty log file if it doesn't exist
    if not os.path.exists(log_file):
        open(log_file, 'a').close()
    
    watch_log_file(log_file)
