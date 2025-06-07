# Grok MCP Server Installation Script for Windows PowerShell
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "Grok MCP Server - Windows Installation" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Gray

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

$versionMatch = [regex]::Match($pythonVersion, "Python (\d+)\.(\d+)")
if ($versionMatch.Success) {
    $major = [int]$versionMatch.Groups[1].Value
    $minor = [int]$versionMatch.Groups[2].Value
    
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
        Write-Host "❌ Python 3.8+ required, found $pythonVersion" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Check if we're in virtual environment
$inVenv = $env:VIRTUAL_ENV -ne $null
if (-not $inVenv) {
    Write-Host "⚠️  Not in virtual environment. Activate it with:" -ForegroundColor Yellow
    Write-Host "    .\venv\Scripts\activate" -ForegroundColor Cyan
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host "✅ Running in virtual environment" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Setup environment file
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env from .env.example" -ForegroundColor Green
    } else {
        @"
XAI_API_KEY=your_api_key_here
DEBUG=false
DEFAULT_MODEL=grok-3-mini-beta
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Created basic .env file" -ForegroundColor Green
    }
    Write-Host "⚠️  Please edit .env and add your XAI_API_KEY" -ForegroundColor Yellow
}

# Test server imports
Write-Host "Testing server startup..." -ForegroundColor Yellow
python -c "import sys; sys.path.insert(0, '.'); from src.server import mcp; print('Server imports successful')"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Server test passed" -ForegroundColor Green
} else {
    Write-Host "❌ Server test failed" -ForegroundColor Red
    exit 1
}

Write-Host "`n$('=' * 60)" -ForegroundColor Gray
Write-Host "✅ Installation completed successfully!" -ForegroundColor Green

# Display Claude configuration
$currentPath = (Get-Location).Path
Write-Host "`nClaude Desktop Configuration:" -ForegroundColor Cyan
Write-Host "Add this to %APPDATA%\Claude\claude_desktop_config.json:" -ForegroundColor Yellow

$config = @"
{
  "mcpServers": {
    "grok": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "$($currentPath -replace '\\', '\\\\')",
      "env": {
        "XAI_API_KEY": "your-xai-api-key-here",
        "PYTHONPATH": "$($currentPath -replace '\\', '\\\\')"
      }
    }
  }
}
"@

Write-Host $config -ForegroundColor White

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your XAI_API_KEY" -ForegroundColor White
Write-Host "2. Copy the configuration above to Claude Desktop" -ForegroundColor White
Write-Host "3. Restart Claude Desktop" -ForegroundColor White