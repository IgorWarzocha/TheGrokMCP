#!/usr/bin/env python3
"""
Grok MCP Server Installation Script
Handles setup, dependency installation, and environment configuration
"""
import subprocess
import sys
import os
import platform
from pathlib import Path
import shutil

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(message, status="info"):
    colors = {"success": Colors.GREEN, "error": Colors.RED, "warning": Colors.YELLOW}
    color = colors.get(status, Colors.BLUE)
    emoji = '✅' if status == 'success' else '❌' if status == 'error' else '⚠️' if status == 'warning' else 'ℹ️'
    print(f"{color}{emoji} {message}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print_status(f"Python 3.8+ required, found {sys.version}", "error")
        return False
    print_status(f"Python {sys.version_info.major}.{sys.version_info.minor} detected", "success")
    return True

def setup_environment():
    """Set up .env file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print_status("Created .env from .env.example", "success")
        else:
            with open(env_file, 'w') as f:
                f.write("XAI_API_KEY=your_api_key_here\n")
                f.write("DEBUG=false\n")
                f.write("DEFAULT_MODEL=grok-3-mini-beta\n")
            print_status("Created basic .env file", "success")
        
        print_status("Please edit .env and add your XAI_API_KEY", "warning")
        return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_api_key_here" in content or "XAI_API_KEY=" not in content:
            print_status("Please set your XAI_API_KEY in .env file", "warning")
            return False
    
    print_status("Environment configuration verified", "success")
    return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        print_status("Installing dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print_status("Dependencies installed successfully", "success")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"Dependency installation failed: {e.stderr}", "error")
        return False

def fix_imports():
    """Fix import statements in the codebase"""
    server_py = Path("src/server.py")
    if server_py.exists():
        content = server_py.read_text()
        # Fix absolute imports to relative
        if "from grok_client import" in content:
            content = content.replace(
                "from grok_client import",
                "from .grok_client import"
            )
            # Fix FastMCP decorators (though they should already be fixed)
            content = content.replace("@mcp.tool\n", "@mcp.tool()\n")
            content = content.replace("@mcp.resource\n", "@mcp.resource()\n") 
            content = content.replace("@mcp.prompt\n", "@mcp.prompt()\n")
            server_py.write_text(content)
            print_status("Fixed import statements and decorators", "success")
        else:
            print_status("Import statements already correct", "success")

def test_server():
    """Test if the server can start"""
    try:
        print_status("Testing server startup...")
        result = subprocess.run([
            sys.executable, "-c", 
            "import sys; sys.path.insert(0, '.'); from src.server import mcp; print('Server imports successful')"
        ], check=True, capture_output=True, text=True, timeout=10)
        print_status("Server test passed", "success")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print_status(f"Server test failed: {getattr(e, 'stderr', str(e))}", "error")
        return False

def create_virtual_env():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print_status("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print_status("Virtual environment created", "success")
            
            # Provide activation instructions
            if platform.system() == "Windows":
                activate_cmd = ".\\venv\\Scripts\\activate"
            else:
                activate_cmd = "source venv/bin/activate"
            
            print_status(f"Activate with: {activate_cmd}", "info")
            return True
        except subprocess.CalledProcessError as e:
            print_status(f"Failed to create virtual environment: {e}", "error")
            return False
    else:
        print_status("Virtual environment already exists", "success")
        return True

def check_virtual_env():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print_status("Not running in virtual environment", "warning")
        print_status("It's recommended to use a virtual environment", "info")
        return False
    print_status("Running in virtual environment", "success")
    return True

def display_claude_config():
    """Display Claude Desktop configuration instructions"""
    print("\n" + "="*60)
    print_status("Claude Desktop Configuration", "info")
    print("\nAdd this to your claude_desktop_config.json:")
    
    current_path = os.path.abspath(".")
    if platform.system() == "Windows":
        current_path = current_path.replace("\\", "\\\\")
    
    config = f'''{{
  "mcpServers": {{
    "grok": {{
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "{current_path}",
      "env": {{
        "XAI_API_KEY": "your-xai-api-key-here",
        "PYTHONPATH": "{current_path}"
      }}
    }}
  }}
}}'''
    print(config)
    
    print("\n" + "="*60)
    print_status("Configuration file locations:", "info")
    print("- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("- Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("- Linux: ~/.config/claude/claude_desktop_config.json")

def main():
    """Main installation process"""
    print_status("Starting Grok MCP Server installation...", "info")
    print("="*60)
    
    if not check_python_version():
        return False
    
    # Suggest virtual environment
    if not check_virtual_env():
        create_virtual_env()
        print_status("Please activate the virtual environment and run install.py again", "warning")
        return True  # Not a failure, just needs manual step
    
    fix_imports()
    
    if not install_dependencies():
        return False
    
    env_ready = setup_environment()
    
    if not test_server():
        return False
    
    print("\n" + "="*60)
    print_status("Installation completed successfully!", "success")
    
    if not env_ready:
        print_status("⚠️  Don't forget to add your XAI_API_KEY to the .env file!", "warning")
    
    print_status("\nNext steps:", "info")
    print("  1. Edit .env file with your XAI_API_KEY (if not done)")
    print("  2. Copy the configuration below to Claude Desktop")
    print("  3. Restart Claude Desktop")
    
    display_claude_config()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\nInstallation cancelled by user", "warning")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")
        sys.exit(1)