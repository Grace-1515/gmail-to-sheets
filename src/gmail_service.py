import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE



def get_gmail_service():
    """
    Authenticates and returns a Gmail API service object.
    Uses OAuth 2.0 and stores token locally for reuse.
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, perform OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_emails(service):
    """
    Fetches unread emails from the inbox.
    Returns a list of message objects.
    """
    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = response.get("messages", [])
    return messages


def mark_email_as_read(service, message_id):
    """
    Marks a Gmail message as read by removing the UNREAD label.
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
