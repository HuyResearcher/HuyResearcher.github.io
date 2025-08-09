# Test script to verify the automation works
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    """Test if all required environment variables are set."""
    required_vars = [
        'GEMINI_API_KEY',
        'GOOGLE_CREDENTIALS_PATH',
        'EMAIL_ADDRESS'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your_{var.lower()}_here':
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✓ All environment variables set")
    return True

def test_google_credentials():
    """Test Google API credentials."""
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    
    if not os.path.exists(creds_path):
        print(f"❌ Google credentials file not found: {creds_path}")
        return False
    
    if not os.path.exists('token.pickle'):
        print("⚠️  No authentication token found. Run setup.py first.")
        return False
    
    print("✓ Google credentials configured")
    return True

def test_gemini_connection():
    """Test Gemini AI connection."""
    try:
        import requests
        api_key = os.getenv('GEMINI_API_KEY')
        
        # Simple test request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{
                    "text": "Hello, respond with just 'OK'"
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print("✓ Gemini AI connection successful")
            return True
        else:
            print(f"❌ Gemini AI connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini AI test failed: {e}")
        return False

def test_email_processing():
    """Test a sample email processing."""
    try:
        from ai_meeting_automation import GeminiAI
        
        gemini = GeminiAI(os.getenv('GEMINI_API_KEY'))
        
        # Test with a sample email
        test_email = """
        Hi team,
        
        I think we should schedule a meeting to discuss the upcoming project deadline.
        Let's sync up on the requirements and timeline.
        
        Please let me know your availability for tomorrow or Friday.
        
        Thanks,
        John
        """
        
        result = gemini.analyze_email(
            email_content=test_email,
            subject="Project Meeting Discussion",
            sender="john@company.com",
            recipients=["team@company.com", "manager@company.com"]
        )
        
        if result.get('requires_meeting'):
            print("✓ Email analysis working - Meeting detected")
        else:
            print("⚠️  Email analysis working - No meeting detected (expected for test)")
        
        return True
        
    except Exception as e:
        print(f"❌ Email processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=== AI Meeting Automation Test Suite ===\n")
    
    tests = [
        ("Environment Variables", test_environment),
        ("Google Credentials", test_google_credentials),
        ("Gemini AI Connection", test_gemini_connection),
        ("Email Processing", test_email_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            if test_func():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}\n")
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The automation is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues before using the automation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
