#!/usr/bin/env python3
"""
Example usage of the Grok MCP Server tools.
This demonstrates how the tools would be called through the MCP protocol.
"""

# Note: These are examples of how the tools would be used through an MCP client.
# In actual usage, these would be called through the MCP protocol by Claude or another client.

# Example 1: Simple chat completion
example_chat_simple = {
    "tool": "chat_completion",
    "arguments": {
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ]
    }
}

# Example 2: Complex reasoning task
example_chat_reasoning = {
    "tool": "chat_completion",
    "arguments": {
        "messages": [
            {"role": "user", "content": "Explain the implications of quantum computing on cryptography"}
        ],
        "task_complexity": "reasoning",
        "temperature": 0.7
    }
}

# Example 3: Code generation with specific model
example_code_generation = {
    "tool": "chat_completion",
    "arguments": {
        "messages": [
            {"role": "system", "content": "You are an expert Python developer."},
            {"role": "user", "content": "Write a function to calculate fibonacci numbers efficiently"}
        ],
        "model": "grok-3",
        "temperature": 0.2,
        "max_tokens": 1000
    }
}

# Example 4: Image understanding
example_image_analysis = {
    "tool": "image_understanding",
    "arguments": {
        "image_path": "/path/to/image.jpg",
        "prompt": "Describe what you see in this image in detail"
    }
}

# Example 5: Create embeddings
example_embeddings = {
    "tool": "create_embeddings",
    "arguments": {
        "texts": [
            "The quick brown fox jumps over the lazy dog",
            "Machine learning is transforming technology",
            "Python is a versatile programming language"
        ]
    }
}

# Example 6: List available models
example_list_models = {
    "tool": "list_models",
    "arguments": {}
}

# Example 7: Multi-turn conversation
example_conversation = {
    "tool": "chat_completion",
    "arguments": {
        "messages": [
            {"role": "user", "content": "I want to learn about machine learning"},
            {"role": "assistant", "content": "Machine learning is a subset of AI that enables systems to learn from data. What aspect would you like to explore?"},
            {"role": "user", "content": "How do neural networks work?"}
        ],
        "model": "grok-3",
        "temperature": 0.8
    }
}

# Example 8: Research task
example_research = {
    "tool": "chat_completion",
    "arguments": {
        "messages": [
            {"role": "user", "content": "Research and summarize the latest developments in renewable energy"}
        ],
        "task_complexity": "research",
        "max_tokens": 2000
    }
}

if __name__ == "__main__":
    print("Grok MCP Server - Usage Examples")
    print("=" * 50)
    print("\nThese examples show how to structure tool calls for the Grok MCP Server.")
    print("In practice, these would be sent through the MCP protocol by Claude or another client.")
    print("\nAvailable tools:")
    print("1. chat_completion - Send messages to Grok")
    print("2. image_understanding - Analyze images")
    print("3. create_embeddings - Generate text embeddings")
    print("4. list_models - Get available models")
    print("\nRefer to the README.md for detailed usage instructions.")