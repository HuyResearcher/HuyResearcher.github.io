#!/usr/bin/env python3
"""
Setup script for Google API credentials and initial configuration.
Run this script first to set up authentication.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def setup_google_credentials():
    """Set up Google API credentials."""
    print("Setting up Google API credentials...")
    
    if not os.path.exists('credentials.json'):
        print("""
        ERROR: credentials.json not found!
        
        To set up Google API access:
        1. Go to https://console.cloud.google.com/
        2. Create a new project or select existing one
        3. Enable Google Calendar API and Gmail API
        4. Go to Credentials → Create Credentials → OAuth 2.0 Client IDs
        5. Choose 'Desktop application'
        6. Download the JSON file and save it as 'credentials.json'
        """)
        return False
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    print("✓ Google API credentials set up successfully!")
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            # Copy example to .env
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("✓ Created .env file from template")
            print("⚠️  Please edit .env file and add your Gemini API key")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✓ .env file already exists")

def check_gemini_api():
    """Check if Gemini API key is configured."""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("""
        ⚠️  Gemini API key not configured!
        
        To get a Gemini API key:
        1. Go to https://makersuite.google.com/app/apikey
        2. Create a new API key
        3. Add it to your .env file: GEMINI_API_KEY=your_actual_key_here
        """)
        return False
    
    print("✓ Gemini API key configured")
    return True

def main():
    """Main setup function."""
    print("=== AI Meeting Automation Setup ===\n")
    
    # Create .env file
    create_env_file()
    
    # Set up Google credentials
    google_ok = setup_google_credentials()
    
    # Check Gemini API
    gemini_ok = check_gemini_api()
    
    print("\n=== Setup Summary ===")
    print(f"Google API: {'✓' if google_ok else '✗'}")
    print(f"Gemini API: {'✓' if gemini_ok else '✗'}")
    
    if google_ok and gemini_ok:
        print("\n🎉 Setup complete! You can now run the automation.")
        print("Run: python ai_meeting_automation.py")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")

if __name__ == "__main__":
    main()
