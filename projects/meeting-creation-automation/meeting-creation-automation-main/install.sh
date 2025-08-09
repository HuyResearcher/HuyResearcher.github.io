#!/bin/bash

# Installation script for the AI Meeting Automation system

echo "=== AI Meeting Automation Installation ==="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python found"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Python dependencies installed"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check if n8n is installed
if ! command -v n8n &> /dev/null; then
    echo "Installing n8n..."
    npm install -g n8n
    
    if [ $? -eq 0 ]; then
        echo "✓ n8n installed"
    else
        echo "❌ Failed to install n8n. Please install Node.js first."
        exit 1
    fi
else
    echo "✓ n8n already installed"
fi

# Run setup script
echo "Running setup script..."
python setup.py

echo ""
echo "=== Next Steps ==="
echo "1. Edit .env file with your API keys"
echo "2. Place your Google credentials.json file in this directory"
echo "3. Run setup again: python setup.py"
echo "4. Start n8n: n8n start"
echo "5. Import the workflow from n8n-workflow.json"
echo "6. Test the automation: python ai_meeting_automation.py"
