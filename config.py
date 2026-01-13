# ---------------------------
# GMAIL API CONFIGURATION
# ---------------------------

# Gmail API scopes
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

# ---------------------------
# GOOGLE SHEETS CONFIGURATION
# ---------------------------

# Google Sheets API scope
SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# Google Sheet details
SPREADSHEET_ID = "PUT_YOUR_SPREADSHEET_ID_HERE"
SHEET_NAME = "Sheet1"

# ---------------------------
# FILE PATHS
# ---------------------------

# OAuth credentials file
CREDENTIALS_FILE = "credentials/credentials.json"

# OAuth token file (generated automatically)
TOKEN_FILE = "token.json"

# State file to store processed email IDs
STATE_FILE = "state.json"
