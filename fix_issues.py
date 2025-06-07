#!/usr/bin/env python3
"""
Quick fix script for common Grok MCP Server issues
"""
import os
import re
from pathlib import Path

def fix_imports():
    """Fix absolute imports to relative imports in server.py"""
    server_file = Path("src/server.py")
    if not server_file.exists():
        print("❌ src/server.py not found!")
        return False
    
    content = server_file.read_text()
    original = content
    
    # Fix the import
    content = re.sub(
        r'^from grok_client import',
        'from .grok_client import',
        content,
        flags=re.MULTILINE
    )
    
    if content != original:
        server_file.write_text(content)
        print("✅ Fixed imports in server.py")
    else:
        print("✅ Imports already correct in server.py")
    
    return True

def fix_decorators():
    """Ensure all MCP decorators have parentheses"""
    fixed_count = 0
    
    for py_file in Path("src").rglob("*.py"):
        content = py_file.read_text()
        original = content
        
        # Fix decorators without parentheses
        content = re.sub(r'@mcp\.tool\s*\n', '@mcp.tool()\n', content)
        content = re.sub(r'@mcp\.resource\s*\n', '@mcp.resource()\n', content)
        content = re.sub(r'@mcp\.prompt\s*\n', '@mcp.prompt()\n', content)
        
        if content != original:
            py_file.write_text(content)
            fixed_count += 1
            print(f"✅ Fixed decorators in {py_file}")
    
    if fixed_count == 0:
        print("✅ All decorators already have correct syntax")
    
    return True

def create_init_files():
    """Ensure all directories have __init__.py files"""
    dirs = ["src", "src/tools", "src/utils", "tests"]
    
    for dir_path in dirs:
        dir_obj = Path(dir_path)
        if dir_obj.exists() and dir_obj.is_dir():
            init_file = dir_obj / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")
                print(f"✅ Created {init_file}")
    
    return True

def verify_env_file():
    """Check and create .env file if needed"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ Created .env from .env.example")
        else:
            env_content = """XAI_API_KEY=your_api_key_here
DEBUG=false
DEFAULT_MODEL=grok-3-mini-beta"""
            env_file.write_text(env_content)
            print("✅ Created default .env file")
        
        print("⚠️  Remember to add your actual API key to .env!")
        return False
    
    print("✅ .env file exists")
    return True

def main():
    """Run all fixes"""
    print("🔧 Applying fixes to Grok MCP Server...")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Apply fixes
    fix_imports()
    fix_decorators()
    create_init_files()
    env_ready = verify_env_file()
    
    print("\n" + "=" * 50)
    print("✅ All fixes applied!")
    
    if not env_ready:
        print("\n⚠️  Don't forget to add your XAI_API_KEY to the .env file!")
    
    print("\nYou can now run:")
    print("  python install.py  # For full installation")
    print("  python run.py      # To start the server")

if __name__ == "__main__":
    main()