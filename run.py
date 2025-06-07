#!/usr/bin/env python3
"""
Simple runner script for the Grok MCP Server.
"""

import sys
from src.server import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down Grok MCP Server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)