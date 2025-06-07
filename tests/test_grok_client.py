"""
Unit tests for the Grok API client.
"""

import pytest
import pytest_asyncio
from unittest.mock import Mock, patch, AsyncMock
import httpx

from src.grok_client import GrokClient, GrokAPIError, GROK_MODELS


class TestGrokClient:
    """Test suite for GrokClient."""
    
    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Mock API key for testing."""
        monkeypatch.setenv("XAI_API_KEY", "test_api_key")
    
    @pytest.fixture
    async def client(self, mock_api_key):
        """Create a test client."""
        async with GrokClient() as client:
            yield client
    
    def test_client_initialization_without_key(self):
        """Test that client raises error without API key."""
        with pytest.raises(ValueError, match="XAI_API_KEY not found"):
            GrokClient()
    
    def test_model_selection(self, mock_api_key):
        """Test model selection based on task complexity."""
        client = GrokClient()
        
        assert client.select_model("simple") == "grok-3-mini-beta"
        assert client.select_model("complex") == "grok-3"
        assert client.select_model("reasoning") == "grok-3-reasoner"
        assert client.select_model("research") == "grok-3-deepsearch"
        assert client.select_model("unknown") == "grok-3-mini-beta"  # default
    
    @pytest.mark.asyncio
    async def test_chat_completion_success(self, client):
        """Test successful chat completion."""
        mock_response = {
            "id": "test_id",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you?"
                }
            }]
        }
        
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = Mock()
            
            result = await client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="grok-3-mini-beta"
            )
            
            assert result == mock_response
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_chat_completion_invalid_model(self, client):
        """Test chat completion with invalid model."""
        with pytest.raises(ValueError, match="Invalid model"):
            await client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="invalid-model"
            )
    
    @pytest.mark.asyncio
    async def test_image_understanding(self, client):
        """Test image understanding functionality."""
        mock_response = {
            "id": "test_id",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "I see a cat in the image."
                }
            }]
        }
        
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = Mock()
            
            result = await client.image_understanding(
                image_data=b"fake_image_data",
                prompt="What do you see?"
            )
            
            assert result == mock_response
    
    @pytest.mark.asyncio
    async def test_embeddings_creation(self, client):
        """Test embeddings creation."""
        mock_response = {
            "data": [{
                "embedding": [0.1, 0.2, 0.3],
                "index": 0
            }]
        }
        
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.raise_for_status = Mock()
            
            result = await client.create_embeddings("Test text")
            
            assert result == mock_response
    
    @pytest.mark.asyncio
    async def test_list_models(self, client):
        """Test listing available models."""
        models = await client.list_models()
        
        assert "models" in models
        assert len(models["models"]) == len(GROK_MODELS)
        assert all("id" in model for model in models["models"])
        assert all("capabilities" in model for model in models["models"])
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, client):
        """Test API error handling."""
        with patch.object(client.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.HTTPStatusError(
                "API Error",
                request=Mock(),
                response=Mock(status_code=400, text="Bad Request")
            )
            
            with pytest.raises(GrokAPIError, match="Chat completion failed"):
                await client.chat_completion(
                    messages=[{"role": "user", "content": "Hello"}]
                )