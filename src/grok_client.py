"""
Grok API Client wrapper with retry logic and comprehensive error handling.
"""

import os
import httpx
import base64
from typing import Dict, List, Optional, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from io import BytesIO
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Available Grok models with their capabilities
GROK_MODELS = {
    "grok-2-latest": {
        "name": "Grok 2 Latest",
        "capabilities": ["chat", "reasoning", "code", "analysis"],
        "context_window": 128000,
        "max_output": 4096
    },
    "grok-3": {
        "name": "Grok 3",
        "capabilities": ["chat", "reasoning", "code", "analysis", "advanced"],
        "context_window": 128000,
        "max_output": 8192
    },
    "grok-3-reasoner": {
        "name": "Grok 3 Reasoner",
        "capabilities": ["chat", "reasoning", "complex_analysis", "multi_step"],
        "context_window": 128000,
        "max_output": 8192
    },
    "grok-3-deepsearch": {
        "name": "Grok 3 DeepSearch",
        "capabilities": ["chat", "research", "web_search", "fact_checking"],
        "context_window": 128000,
        "max_output": 8192
    },
    "grok-3-mini-beta": {
        "name": "Grok 3 Mini Beta",
        "capabilities": ["chat", "basic_reasoning", "code"],
        "context_window": 64000,
        "max_output": 4096
    }
}


class GrokAPIError(Exception):
    """Custom exception for Grok API errors."""
    pass


class GrokClient:
    """Client for interacting with the Grok API."""
    
    BASE_URL = "https://api.x.ai/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Grok client with API key."""
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found in environment variables")
        
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()
    
    def select_model(self, task_complexity: str = "simple") -> str:
        """
        Select appropriate Grok model based on task complexity.
        
        Args:
            task_complexity: 'simple', 'complex', 'reasoning', 'research'
            
        Returns:
            Model identifier string
        """
        model_map = {
            "simple": "grok-3-mini-beta",
            "complex": "grok-3",
            "reasoning": "grok-3-reasoner",
            "research": "grok-3-deepsearch"
        }
        return model_map.get(task_complexity, "grok-3-mini-beta")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a chat completion with retry logic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Grok model to use (defaults to grok-3-mini-beta)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            stream: Whether to stream the response
            
        Returns:
            API response dictionary
        """
        if model is None:
            model = os.getenv("DEFAULT_MODEL", "grok-3-mini-beta")
        
        if model not in GROK_MODELS:
            raise ValueError(f"Invalid model: {model}. Available models: {list(GROK_MODELS.keys())}")
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise GrokAPIError(f"Chat completion failed: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise GrokAPIError(f"Unexpected error: {str(e)}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def image_understanding(
        self,
        image_data: Union[str, bytes],
        prompt: str,
        model: str = "grok-2-latest"
    ) -> Dict[str, Any]:
        """
        Analyze an image with Grok's vision capabilities.
        
        Args:
            image_data: Base64 encoded image string or raw bytes
            prompt: Question or instruction about the image
            model: Grok model to use (must support vision)
            
        Returns:
            API response dictionary
        """
        # Convert image to base64 if needed
        if isinstance(image_data, bytes):
            image_data = base64.b64encode(image_data).decode('utf-8')
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ]
            }
        ]
        
        return await self.chat_completion(messages, model=model)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def create_embeddings(
        self,
        texts: Union[str, List[str]],
        model: str = "text-embedding-3-small"
    ) -> Dict[str, Any]:
        """
        Create embeddings for text(s).
        
        Args:
            texts: Single text or list of texts to embed
            model: Embedding model to use
            
        Returns:
            API response with embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/embeddings",
                json={
                    "model": model,
                    "input": texts
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise GrokAPIError(f"Embeddings creation failed: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise GrokAPIError(f"Unexpected error: {str(e)}")
    
    async def list_models(self) -> Dict[str, Any]:
        """
        List available Grok models with their capabilities.
        
        Returns:
            Dictionary of available models and their metadata
        """
        return {
            "models": [
                {
                    "id": model_id,
                    **metadata
                }
                for model_id, metadata in GROK_MODELS.items()
            ]
        }