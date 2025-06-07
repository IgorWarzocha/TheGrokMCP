# Grok MCP Server 🚀

A production-ready Model Context Protocol (MCP) server for Grok AI models, built with FastMCP for clean, Pythonic implementation. Developed using my own [Superprompt System](https://github.com/IgorWarzocha/Claude-Superprompt-System)

Created by **Igor Warzocha** | [LinkedIn](https://www.linkedin.com/in/igorwarzocha/) | [GitHub](https://github.com/IgorWarzocha/Claude-Superprompt-System)

## ☕ Support This Project

If this has helped you, consider buying me a coffee so I can finance my Opus credits!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K31G2HFS)

Your support helps me create more AI optimization resources and keep this project updated!

## Features

- **Full Model Support**: Access to all Grok models (grok-2-latest, grok-3, grok-3-reasoner, grok-3-deepsearch, grok-3-mini-beta)
- **Intelligent Model Selection**: Automatically choose the best model based on task complexity
- **Vision Capabilities**: Analyze images with Grok's visual understanding
- **Text Embeddings**: Generate embeddings for semantic search and analysis
- **Retry Logic**: Built-in exponential backoff for robust API interactions
- **Comprehensive Error Handling**: Detailed error messages and graceful degradation
- **FastMCP Integration**: Clean, decorator-based API for easy extension

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/IgorWarzocha/TheGrokMCP.git
cd TheGrokMCP

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Grok API key
# XAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Server

```bash
# Run the MCP server
python -m src.server

# Or with debug logging
DEBUG=true python -m src.server
```

### 4. Connect with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "grok": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/TheGrokMCP",
      "env": {
        "XAI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Available Tools

### 1. chat_completion

Send chat messages to Grok with intelligent model selection.

```python
# Simple chat
await chat_completion([{"role": "user", "content": "Hello!"}])

# Auto-select model based on complexity
await chat_completion(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    task_complexity="complex"  # Options: simple, complex, reasoning, research
)

# Use specific model
await chat_completion(
    messages=[{"role": "user", "content": "Solve this puzzle"}],
    model="grok-3-reasoner"
)
```

### 2. image_understanding

Analyze images using Grok's vision capabilities.

```python
# From file path
await image_understanding(
    image_path="/path/to/image.jpg",
    prompt="What's in this image?"
)

# From base64 data
await image_understanding(
    image_base64="base64_encoded_data",
    prompt="Describe the scene"
)
```

### 3. create_embeddings

Generate text embeddings for semantic analysis.

```python
# Single text
await create_embeddings("Hello world")

# Multiple texts
await create_embeddings([
    "First document",
    "Second document",
    "Third document"
])
```

### 4. list_models

Get information about all available Grok models.

```python
models = await list_models()
# Returns model capabilities, context windows, and specifications
```

## Model Comparison

| Model | Best For | Context Window | Max Output |
|-------|----------|----------------|------------|
| grok-3-mini-beta | Quick responses, simple tasks | 64,000 | 4,096 |
| grok-2-latest | General purpose, image analysis | 128,000 | 4,096 |
| grok-3 | Complex tasks, advanced features | 128,000 | 8,192 |
| grok-3-reasoner | Multi-step reasoning, analysis | 128,000 | 8,192 |
| grok-3-deepsearch | Research, fact-checking | 128,000 | 8,192 |

## Configuration Options

### Environment Variables

- `XAI_API_KEY` (required): Your Grok API key
- `DEFAULT_MODEL` (optional): Default model to use (default: grok-3-mini-beta)
- `DEBUG` (optional): Enable debug logging (default: false)

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: XAI_API_KEY not found in environment variables
   ```
   Solution: Ensure your `.env` file contains `XAI_API_KEY=your_key_here`

2. **Model Not Available**
   ```
   Error: Invalid model: grok-4
   ```
   Solution: Use `list_models()` to see available models

3. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   ```
   Solution: The client includes automatic retry with exponential backoff

4. **Image Analysis Fails**
   ```
   Error: Image file not found
   ```
   Solution: Ensure the image path is absolute or use base64 encoding

### Debug Mode

Enable detailed logging:

```bash
DEBUG=true python -m src.server
```

## Development

### Project Structure

```
TheGrokMCP/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── grok_client.py     # Grok API client
│   └── utils/             # Helper utilities
├── tests/                 # Test suite
├── docs/                  # Additional documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
└── TODO.md               # Development roadmap
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

### Adding New Tools

1. Add the tool to `server.py` using the `@mcp.tool` decorator:

```python
@mcp.tool
async def my_new_tool(param1: str, param2: int) -> Dict[str, Any]:
    """Tool description here."""
    # Implementation
    pass
```

2. Update the README with usage examples
3. Add tests for the new functionality

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/IgorWarzocha/TheGrokMCP/issues)
- Documentation: See the `docs/` directory for detailed guides
- API Reference: [Grok API Documentation](https://docs.x.ai/api)

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) - The Pythonic way to build MCP servers
- Powered by [Grok AI](https://x.ai) - Advanced AI models by xAI
