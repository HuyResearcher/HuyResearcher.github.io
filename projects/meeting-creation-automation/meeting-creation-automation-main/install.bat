@echo off
REM Installation script for Windows

echo === AI Meeting Automation Installation ===

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    exit /b 1
)

echo ✓ Python found

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    exit /b 1
)

echo ✓ Python dependencies installed

REM Check if n8n is installed
n8n --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing n8n...
    npm install -g n8n
    
    if %errorlevel% neq 0 (
        echo ❌ Failed to install n8n. Please install Node.js first.
        exit /b 1
    )
    
    echo ✓ n8n installed
) else (
    echo ✓ n8n already installed
)

REM Run setup script
echo Running setup script...
python setup.py

echo.
echo === Next Steps ===
echo 1. Edit .env file with your API keys
echo 2. Place your Google credentials.json file in this directory
echo 3. Run setup again: python setup.py
echo 4. Start n8n: n8n start
echo 5. Import the workflow from n8n-workflow.json
echo 6. Test the automation: python ai_meeting_automation.py

pause
