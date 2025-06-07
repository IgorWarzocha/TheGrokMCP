"""
Grok MCP Server - A comprehensive MCP server for Grok AI models.
Built with FastMCP for clean, Pythonic implementation.
"""

import os
import base64
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import asyncio

from fastmcp import FastMCP
from dotenv import load_dotenv

from .grok_client import GrokClient, GrokAPIError, GROK_MODELS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    "Grok MCP Server 🚀",
    version="1.0.0"
)


@mcp.tool()
async def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    task_complexity: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    Send a chat completion request to Grok.
    
    Args:
        messages: List of message dicts with 'role' and 'content' keys
        model: Specific Grok model to use (e.g., 'grok-3', 'grok-3-reasoner')
        task_complexity: Auto-select model based on complexity ('simple', 'complex', 'reasoning', 'research')
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens in response
    
    Returns:
        Response from Grok API including the generated text
    
    Examples:
        Simple chat:
        >>> await chat_completion([{"role": "user", "content": "Hello!"}])
        
        Complex reasoning:
        >>> await chat_completion(
        ...     [{"role": "user", "content": "Explain quantum computing"}],
        ...     task_complexity="complex"
        ... )
    """
    try:
        async with GrokClient() as client:
            # Auto-select model if task_complexity is provided
            if task_complexity and not model:
                model = client.select_model(task_complexity)
                logger.info(f"Auto-selected model: {model} for {task_complexity} task")
            
            # Use default model if none specified
            if not model:
                model = os.getenv("DEFAULT_MODEL", "grok-3-mini-beta")
            
            logger.info(f"Sending chat completion request with model: {model}")
            
            response = await client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "success": True,
                "model_used": model,
                "response": response
            }
            
    except GrokAPIError as e:
        logger.error(f"Grok API error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_error"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "unexpected_error"
        }


@mcp.tool()
async def image_understanding(
    image_path: Optional[str] = None,
    image_base64: Optional[str] = None,
    prompt: str = "What do you see in this image?",
    model: str = "grok-2-latest"
) -> Dict[str, Any]:
    """
    Analyze an image using Grok's vision capabilities.
    
    Args:
        image_path: Path to local image file
        image_base64: Base64 encoded image data
        prompt: Question or instruction about the image
        model: Grok model to use (must support vision)
    
    Returns:
        Grok's analysis of the image
    
    Note: Provide either image_path OR image_base64, not both.
    """
    try:
        async with GrokClient() as client:
            # Handle image input
            if image_path:
                with open(image_path, "rb") as f:
                    image_data = f.read()
            elif image_base64:
                image_data = base64.b64decode(image_base64)
            else:
                return {
                    "success": False,
                    "error": "Must provide either image_path or image_base64",
                    "error_type": "input_error"
                }
            
            logger.info(f"Analyzing image with model: {model}")
            
            response = await client.image_understanding(
                image_data=image_data,
                prompt=prompt,
                model=model
            )
            
            return {
                "success": True,
                "model_used": model,
                "response": response
            }
            
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"Image file not found: {image_path}",
            "error_type": "file_error"
        }
    except GrokAPIError as e:
        logger.error(f"Grok API error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_error"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "unexpected_error"
        }


@mcp.tool()
async def create_embeddings(
    texts: Union[str, List[str]],
    model: str = "text-embedding-3-small"
) -> Dict[str, Any]:
    """
    Create embeddings for text(s) using Grok's embedding models.
    
    Args:
        texts: Single text string or list of texts to embed
        model: Embedding model to use
    
    Returns:
        Embeddings for the provided text(s)
    """
    try:
        async with GrokClient() as client:
            logger.info(f"Creating embeddings for {len(texts) if isinstance(texts, list) else 1} text(s)")
            
            response = await client.create_embeddings(
                texts=texts,
                model=model
            )
            
            return {
                "success": True,
                "model_used": model,
                "embeddings": response
            }
            
    except GrokAPIError as e:
        logger.error(f"Grok API error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_error"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "unexpected_error"
        }


@mcp.tool()
async def list_models() -> Dict[str, Any]:
    """
    List all available Grok models with their capabilities and specifications.
    
    Returns:
        Dictionary containing available models and their metadata
    """
    try:
        async with GrokClient() as client:
            models = await client.list_models()
            
            return {
                "success": True,
                "models": models["models"],
                "model_count": len(models["models"])
            }
            
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to list models: {str(e)}",
            "error_type": "unexpected_error"
        }


# Resources (optional) - Expose model information as resources
@mcp.resource("models://available")
async def get_available_models() -> str:
    """Get information about available Grok models."""
    models_info = []
    for model_id, info in GROK_MODELS.items():
        models_info.append(f"## {info['name']} ({model_id})")
        models_info.append(f"- Capabilities: {', '.join(info['capabilities'])}")
        models_info.append(f"- Context Window: {info['context_window']:,} tokens")
        models_info.append(f"- Max Output: {info['max_output']:,} tokens")
        models_info.append("")
    
    return "\n".join(models_info)


# Prompts (optional) - Define reusable prompt templates
@mcp.prompt("code_review")
async def code_review_prompt(language: str = "Python", focus: str = "general") -> str:
    """Generate a code review prompt template."""
    return f"""You are an expert {language} code reviewer. Please review the provided code with a focus on {focus}.

Consider:
1. Code quality and readability
2. Performance implications
3. Security concerns
4. Best practices
5. Potential bugs or edge cases

Provide constructive feedback with specific suggestions for improvement."""


@mcp.prompt("reasoning_task")
async def reasoning_task_prompt(task_type: str = "analysis") -> str:
    """Generate a reasoning task prompt template."""
    return f"""You are tasked with a {task_type} that requires careful reasoning.

Please:
1. Break down the problem into clear components
2. Consider multiple perspectives or approaches
3. Apply logical reasoning step by step
4. Identify any assumptions being made
5. Provide a well-reasoned conclusion

Be thorough and explain your reasoning process clearly."""


# Entry point
def main():
    """Run the Grok MCP server."""
    # Check for API key
    if not os.getenv("XAI_API_KEY"):
        logger.error("XAI_API_KEY not found in environment variables!")
        logger.error("Please set your Grok API key in the .env file or environment")
        return
    
    logger.info("Starting Grok MCP Server...")
    logger.info(f"Available models: {', '.join(GROK_MODELS.keys())}")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()