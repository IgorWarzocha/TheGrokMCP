# Quick Setup Guide for Grok MCP Server

## Prerequisites

- Python 3.8 or higher
- Grok API key from [x.ai](https://x.ai)
- Claude Desktop app

## Step-by-Step Setup

### 1. Clone and Install

```bash
# Clone the repository (or copy the files)
cd /path/to/your/projects
cp -r /tmp/TheGrokMCP .
cd TheGrokMCP

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
nano .env  # or use your preferred editor
```

Add your key:
```
XAI_API_KEY=xai-your-actual-api-key-here
```

### 3. Test the Server

```bash
# Run the server directly
python run.py

# Or use the module
python -m src.server

# With debug mode
DEBUG=true python run.py
```

You should see:
```
Starting Grok MCP Server...
Available models: grok-2-latest, grok-3, grok-3-reasoner, grok-3-deepsearch, grok-3-mini-beta
```

### 4. Configure Claude Desktop

Find your Claude Desktop configuration file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`

Add the Grok MCP server:

```json
{
  "mcpServers": {
    "grok": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/full/path/to/TheGrokMCP",
      "env": {
        "XAI_API_KEY": "xai-your-api-key-here",
        "PYTHONPATH": "/full/path/to/TheGrokMCP"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

After saving the configuration, restart Claude Desktop. You should now be able to use Grok tools!

## Testing in Claude

Try these commands in Claude:

1. **Basic chat:**
   "Use Grok to explain what MCP servers are"

2. **Complex reasoning:**
   "Use Grok's reasoning model to solve this logic puzzle..."

3. **List models:**
   "What Grok models are available?"

4. **Image analysis:**
   "Use Grok to analyze this image [attach image]"

## Troubleshooting

### Server won't start
- Check Python version: `python --version` (needs 3.8+)
- Verify API key is set correctly in .env
- Check dependencies: `pip list`

### Claude can't connect
- Verify the path in claude_desktop_config.json is absolute
- Check the server runs standalone first
- Look for errors in Claude's developer console

### API errors
- Verify your API key is valid at [x.ai](https://x.ai)
- Check you have API credits available
- Enable debug mode to see detailed errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [TODO.md](TODO.md) for planned features
- Run tests: `pytest` (after installing dev dependencies)
- Contribute improvements via pull requests!

Need help? Open an issue on GitHub!