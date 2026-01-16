Gmail to Google Sheets Automation (Python)

Author
Grace Emima

Project Overview

This project is a Python automation system that connects to the Gmail API and Google Sheets API using OAuth 2.0 authentication.
It reads unread emails from a Gmail inbox and logs their details into a Google Sheet while ensuring no duplicate entries.

The script is designed to be safe to re-run multiple times without reprocessing the same emails.

Objective

Each unread email is appended as a new row in Google Sheets with the following fields:

From
Sender email address

Subject
Email subject

Date
Date and time received

Content
Email body in plain text

High Level Architecture

Gmail Inbox with unread emails
Data is accessed through Gmail API using OAuth 2.0
Emails are parsed using Python logic
Duplicate check is performed using a local state file
Data is sent to Google Sheets using Sheets API
Rows are appended to the Google Sheet

Technology Stack

Language
Python 3

APIs Used
Gmail API
Google Sheets API

Authentication
OAuth 2.0 Desktop Application

Libraries
google-api-python-client
google-auth
google-auth-oauthlib

Project Structure

gmail-to-sheets
src
gmail_service.py
sheets_service.py
email_parser.py
main.py

credentials
credentials.json ignored in git

config.py
state.json ignored in git
token.json ignored in git
requirements.txt
README.md
.gitignore

OAuth 2.0 Authentication Flow

A Google Cloud project is created.
Gmail API and Google Sheets API are enabled.
OAuth consent screen is configured.
A Desktop OAuth client ID is created.

On the first execution, a browser window opens for login.
The user grants permission for Gmail and Google Sheets access.
An OAuth token is generated and stored locally.

On subsequent runs, the stored token is reused and login is not required again.

Sensitive files such as credentials and tokens are excluded using gitignore.

Duplicate Prevention Logic

Each Gmail message has a unique message ID.
After an email is processed, its message ID is stored in a local state file.

Before processing any email, the script checks whether the message ID already exists.
If it exists, the email is skipped.
If it does not exist, the email is processed and logged.

This ensures that no duplicate rows are added even if the script is run multiple times.

State Persistence

State is stored locally in a file called state.json.

The file contains a list of processed message IDs.

This approach was chosen because it is simple, transparent, does not require a database, and persists across script executions.

How to Run

Activate the virtual environment.

venv\Scripts\Activate.ps1

Run the script.

python src/main.py

On the first run, OAuth authorization will be requested in the browser.
On later runs, the script executes automatically using the saved token.

Proof of Execution

The proof folder contains screenshots and a short video demonstration showing:

Unread emails in Gmail
Rows populated in Google Sheets
OAuth consent screen
End to end execution flow

Challenges Faced

OAuth Scope Issues
Initially the OAuth token did not include Google Sheets permissions.
This was resolved by unifying Gmail and Sheets scopes and regenerating the token.

Google Sheets API 404 Errors
Google Drive storage was full which made the spreadsheet non editable.
This caused the API to return a 404 error.
Freeing storage resolved the issue.

Repeated Email Processing
Emails were not being marked as read correctly.
This was fixed by explicitly removing the UNREAD label using the Gmail API.

Limitations

Only unread emails from the inbox are processed.
Email content is stored as plain text only.
State is stored locally and is not distributed.
The solution is not designed for very large email volumes.

Possible Enhancements

Subject based filtering
HTML to plain text conversion
Logging with timestamps
Retry logic for API failures
Docker based deployment

Post Submission Change Readiness

The modular design allows quick changes such as:

Processing emails from a specific time range
Adding new columns such as labels
Excluding automated or no reply emails

Project Status

Gmail API integration completed
Google Sheets API integration completed
OAuth 2.0 authentication implemented
Duplicate prevention implemented
End to end automation working
