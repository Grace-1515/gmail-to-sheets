import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import json
from gmail_service import get_gmail_service, fetch_unread_emails, mark_email_as_read
from sheets_service import get_sheets_service, append_row
from email_parser import parse_email
from config import STATE_FILE


def load_state():
    print("Reading state file from:", os.path.abspath(STATE_FILE))
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"processed_ids": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    state = load_state()
    processed_ids = set(state.get("processed_ids", []))

    messages = fetch_unread_emails(gmail_service)

    if not messages:
        print("No unread emails found.")
        return

    for msg in messages:
        msg_id = msg["id"]
        

        # Duplicate prevention
        if msg_id in processed_ids:
            continue

        # Fetch full message
        message = gmail_service.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        sender, subject, date, content = parse_email(message)

        # Append to Google Sheets
        append_row(
            sheets_service,
            [sender, subject, date, content]
        )

        # Mark email as read
        mark_email_as_read(gmail_service, msg_id)

        # Update state
        processed_ids.add(msg_id)
        

    save_state({"processed_ids": list(processed_ids)})
    print("Processing completed successfully.")


if __name__ == "__main__":
    main()
