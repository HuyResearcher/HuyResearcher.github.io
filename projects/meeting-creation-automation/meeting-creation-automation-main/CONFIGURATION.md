# AI Meeting Automation Configuration Guide

## 🔧 Detailed Configuration

### 1. Google Cloud Setup

#### Enable APIs:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Navigate to "APIs & Services" → "Enable APIs and Services"
4. Enable the following APIs:
   - Google Calendar API
   - Gmail API

#### Create Credentials:
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the JSON file as `credentials.json`

### 2. Gemini AI Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Add to your `.env` file

### 3. n8n Workflow Configuration

#### Import Workflow:
1. Start n8n: `n8n start`
2. Open browser to `http://localhost:5678`
3. Click "Import from file"
4. Select `n8n-workflow.json`
5. Activate the workflow

#### Customize Nodes:

**Trigger Node (Email Check):**
- Interval: Every 5 minutes (adjustable)
- Can be changed to webhook trigger for real-time processing

**Python Processor Node:**
- Command: `python ai_meeting_automation.py`
- Working Directory: Set to project path
- Environment variables: Loaded from .env

**Conditional Node (Meeting Check):**
- Condition: `meeting_created === true`
- Routes to notification or logging

### 4. Advanced Customization

#### Email Filters:
```python
# In ai_meeting_automation.py
def get_recent_emails(self, max_results: int = 10) -> List[Dict]:
    # Add custom query filters
    query = 'is:unread -label:automated -from:noreply'
    results = self.gmail_service.users().messages().list(
        userId='me',
        maxResults=max_results,
        q=query  # Custom filter
    ).execute()
```

#### AI Prompt Customization:
```python
# Modify the analyze_email prompt for different behavior
prompt = f"""
Your custom prompt here...
Consider company-specific keywords: {custom_keywords}
Meeting types: {meeting_types}
"""
```

#### Meeting Scheduling Logic:
```python
def _get_next_business_day_time(self) -> datetime:
    # Custom scheduling logic
    # Consider business hours, time zones, holidays
    pass
```

### 5. Security Considerations

- Store API keys in environment variables only
- Use OAuth 2.0 for Google APIs (no hardcoded credentials)
- Regularly rotate API keys
- Limit API access scopes to minimum required
- Monitor API usage and quotas

### 6. Performance Optimization

#### Email Processing:
- Batch process emails in groups
- Use pagination for large email volumes
- Cache processed email IDs
- Implement rate limiting

#### API Usage:
- Use exponential backoff for retries
- Monitor quota usage
- Cache calendar events
- Optimize prompt length for Gemini AI

### 7. Error Handling

#### Common Error Scenarios:
```python
# API Rate Limits
try:
    response = api_call()
except HttpError as error:
    if error.resp.status == 429:  # Too Many Requests
        time.sleep(60)  # Wait and retry
        
# Authentication Issues
if not creds.valid:
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Re-authenticate
        flow = InstalledAppFlow.from_client_secrets_file(...)
```

### 8. Monitoring Setup

#### Logging Configuration:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
```

#### Metrics Tracking:
- Emails processed per hour
- Meeting creation success rate
- AI confidence scores distribution
- API response times

### 9. Deployment Options

#### Local Development:
- Run on personal machine
- Use ngrok for webhook endpoints
- Manual monitoring

#### Server Deployment:
- Deploy on VPS/cloud server
- Use systemd service for auto-restart
- Set up log rotation
- Configure monitoring alerts

#### Docker Deployment:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "ai_meeting_automation.py"]
```

### 10. Testing Strategy

#### Unit Tests:
- Test individual components
- Mock external API calls
- Verify email parsing logic

#### Integration Tests:
- End-to-end workflow testing
- API connectivity tests
- Authentication flow testing

#### Load Testing:
- High email volume scenarios
- API rate limit testing
- Concurrent processing tests
