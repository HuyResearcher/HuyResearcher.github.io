import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
from dotenv import load_dotenv

load_dotenv()

class GeminiAI:
    """Gemini AI client for email analysis and meeting decision making."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def analyze_email(self, email_content: str, subject: str, sender: str, recipients: List[str]) -> Dict:
        """
        Analyze email content to determine if a meeting should be created.
        Returns structured data about the meeting requirements.
        """
        prompt = f"""
        Analyze the following email and determine if it requires creating a Google Meet:

        Subject: {subject}
        Sender: {sender}
        Recipients: {', '.join(recipients)}
        Content: {email_content}

        Please analyze and return a JSON response with the following structure:
        {{
            "requires_meeting": true/false,
            "meeting_title": "extracted or suggested meeting title",
            "meeting_description": "brief description of the meeting purpose",
            "suggested_duration": 60, // in minutes
            "urgency": "high/medium/low",
            "participants": ["email1@domain.com", "email2@domain.com"], // all emails that should be invited
            "suggested_time": "YYYY-MM-DD HH:MM", // if mentioned in email, otherwise null
            "meeting_type": "discussion/presentation/review/standup/other",
            "key_topics": ["topic1", "topic2"], // main discussion points
            "confidence_score": 0.85 // how confident you are about needing a meeting (0-1)
        }}

        Look for keywords like: "meeting", "call", "discuss", "sync", "standup", "review", "presentation", 
        "let's talk", "schedule", "catch up", "urgent", etc.

        Only suggest a meeting if:
        1. The email explicitly requests a meeting or discussion
        2. The content suggests coordination is needed
        3. Multiple people need to be aligned on something
        4. There's a decision that requires group input
        5. There's urgency that requires immediate attention

        Do NOT suggest meetings for:
        - Simple information sharing
        - FYI emails
        - Automated notifications
        - Thank you messages
        - Simple confirmations
        """

        headers = {
            "Content-Type": "application/json",
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            # Extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found in AI response")
                
        except Exception as e:
            print(f"Error calling Gemini AI: {e}")
            return {
                "requires_meeting": False,
                "error": str(e)
            }

class GoogleCalendarManager:
    """Manages Google Calendar and Meet operations."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.readonly'
    ]
    
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.creds = None
        self.calendar_service = None
        self.gmail_service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google APIs."""
        token_path = 'token.pickle'
        
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
    
    def create_meeting(self, meeting_data: Dict) -> Dict:
        """Create a Google Calendar event with Google Meet."""
        try:
            # Calculate meeting time
            if meeting_data.get('suggested_time'):
                start_time = datetime.strptime(meeting_data['suggested_time'], '%Y-%m-%d %H:%M')
            else:
                # Default to next business day at 2 PM
                start_time = self._get_next_business_day_time()
            
            end_time = start_time + timedelta(minutes=meeting_data.get('suggested_duration', 60))
            
            # Prepare attendees
            attendees = []
            for email in meeting_data.get('participants', []):
                attendees.append({'email': email})
            
            # Create event
            event = {
                'summary': meeting_data.get('meeting_title', 'AI Generated Meeting'),
                'description': f"{meeting_data.get('meeting_description', '')}\n\n"
                              f"Meeting Type: {meeting_data.get('meeting_type', 'discussion')}\n"
                              f"Key Topics: {', '.join(meeting_data.get('key_topics', []))}\n\n"
                              f"This meeting was automatically created by AI automation.",
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': attendees,
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"ai-meeting-{datetime.now().timestamp()}",
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 15},      # 15 minutes before
                    ],
                },
            }
            
            created_event = self.calendar_service.events().insert(
                calendarId=os.getenv('CALENDAR_ID', 'primary'),
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink'),
                'meet_link': created_event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri'),
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return {'success': False, 'error': str(error)}
    
    def _get_next_business_day_time(self) -> datetime:
        """Get next business day at 2 PM."""
        now = datetime.now()
        days_ahead = 1
        
        # Find next weekday
        while (now + timedelta(days=days_ahead)).weekday() > 4:  # 0-4 are Mon-Fri
            days_ahead += 1
        
        next_day = now + timedelta(days=days_ahead)
        return next_day.replace(hour=14, minute=0, second=0, microsecond=0)
    
    def get_recent_emails(self, max_results: int = 10) -> List[Dict]:
        """Get recent emails for processing."""
        try:
            results = self.gmail_service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q='is:unread'  # Only unread emails
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()
                
                payload = msg['payload']
                headers = payload.get('headers', [])
                
                # Extract email metadata
                email_data = {
                    'id': message['id'],
                    'thread_id': msg['threadId'],
                    'snippet': msg['snippet']
                }
                
                for header in headers:
                    name = header['name'].lower()
                    if name == 'subject':
                        email_data['subject'] = header['value']
                    elif name == 'from':
                        email_data['sender'] = header['value']
                    elif name == 'to':
                        email_data['to'] = header['value']
                    elif name == 'cc':
                        email_data['cc'] = header['value']
                    elif name == 'date':
                        email_data['date'] = header['value']
                
                # Get email body
                email_data['body'] = self._extract_email_body(payload)
                emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []
    
    def _extract_email_body(self, payload) -> str:
        """Extract email body from payload."""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = self._decode_base64(data)
                    break
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = self._decode_base64(data)
        
        return body
    
    def _decode_base64(self, data: str) -> str:
        """Decode base64 encoded email content."""
        import base64
        return base64.urlsafe_b64decode(data).decode('utf-8')

class EmailProcessor:
    """Main email processing and automation class."""
    
    def __init__(self):
        self.gemini = GeminiAI(os.getenv('GEMINI_API_KEY'))
        self.calendar_manager = GoogleCalendarManager(os.getenv('GOOGLE_CREDENTIALS_PATH'))
        self.processed_emails = set()
    
    def process_emails(self) -> List[Dict]:
        """Process recent emails and create meetings as needed."""
        emails = self.calendar_manager.get_recent_emails(
            max_results=int(os.getenv('MAX_EMAILS_PER_CHECK', 50))
        )
        
        results = []
        
        for email in emails:
            if email['id'] in self.processed_emails:
                continue
            
            try:
                # Extract recipients
                recipients = []
                if email.get('to'):
                    recipients.extend(self._extract_emails(email['to']))
                if email.get('cc'):
                    recipients.extend(self._extract_emails(email['cc']))
                
                # Analyze email with AI
                analysis = self.gemini.analyze_email(
                    email_content=email.get('body', ''),
                    subject=email.get('subject', ''),
                    sender=email.get('sender', ''),
                    recipients=recipients
                )
                
                result = {
                    'email_id': email['id'],
                    'subject': email.get('subject', ''),
                    'sender': email.get('sender', ''),
                    'analysis': analysis,
                    'meeting_created': False
                }
                
                # Create meeting if required
                if analysis.get('requires_meeting') and analysis.get('confidence_score', 0) > 0.7:
                    meeting_result = self.calendar_manager.create_meeting(analysis)
                    result['meeting_result'] = meeting_result
                    result['meeting_created'] = meeting_result.get('success', False)
                
                results.append(result)
                self.processed_emails.add(email['id'])
                
            except Exception as e:
                print(f"Error processing email {email['id']}: {e}")
                results.append({
                    'email_id': email['id'],
                    'error': str(e),
                    'meeting_created': False
                })
        
        return results
    
    def _extract_emails(self, email_string: str) -> List[str]:
        """Extract email addresses from a string."""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, email_string)

if __name__ == "__main__":
    processor = EmailProcessor()
    results = processor.process_emails()
    
    print(f"Processed {len(results)} emails")
    for result in results:
        if result.get('meeting_created'):
            print(f"Created meeting for: {result['subject']}")
        else:
            print(f"No meeting needed for: {result['subject']}")
