#!/usr/bin/env python3
"""
Environment checker for Grok MCP Server
Ensures proper virtual environment usage and configuration
"""
import sys
import os
from pathlib import Path

def ensure_virtual_environment():
    """Ensure we're running in a virtual environment"""
    if not hasattr(sys, 'real_prefix') and not (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    ):
        print("❌ Not running in a virtual environment!")
        print("Please create and activate a virtual environment:")
        print("  python -m venv venv")
        if os.name == 'nt':  # Windows
            print("  .\\venv\\Scripts\\activate")
        else:  # Unix-like
            print("  source venv/bin/activate")
        sys.exit(1)
    print("✅ Virtual environment detected")

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastmcp',
        'httpx',
        'dotenv',
        'tenacity',
        'PIL',
        'numpy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("✅ All required packages installed")

def check_env_file():
    """Check if .env file exists and has API key"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please create one from .env.example or run install.py")
        sys.exit(1)
    
    with open(env_file, 'r') as f:
        content = f.read()
        if "XAI_API_KEY" not in content:
            print("❌ XAI_API_KEY not found in .env file!")
            sys.exit(1)
        if "your_api_key_here" in content:
            print("⚠️  Please replace 'your_api_key_here' with your actual API key")
            sys.exit(1)
    
    print("✅ Environment file configured")

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required, found {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def main():
    """Run all environment checks"""
    print("Grok MCP Server - Environment Check")
    print("=" * 40)
    
    check_python_version()
    ensure_virtual_environment()
    check_dependencies()
    check_env_file()
    
    print("\n✅ All checks passed! Environment is ready.")
    print("\nYou can now run the server with:")
    print("  python run.py")
    print("  # or")
    print("  python -m src.server")

if __name__ == "__main__":
    main()