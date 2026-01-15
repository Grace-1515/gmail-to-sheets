import base64
from bs4 import BeautifulSoup


def _get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def parse_email(message):
    """
    Extracts sender, subject, date, and body from a Gmail message.
    Returns a tuple: (from, subject, date, content)
    """
    payload = message["payload"]
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date = _get_header(headers, "Date")

    body = ""

    # Case 1: simple email (body directly available)
    if "body" in payload and payload["body"].get("data"):
        body = payload["body"]["data"]

    # Case 2: multipart email
    elif "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") in ["text/plain", "text/html"]:
                body = part["body"].get("data")
                if body:
                    break

    if body:
        body = base64.urlsafe_b64decode(body).decode("utf-8", errors="ignore")
        body = BeautifulSoup(body, "html.parser").get_text()

    return sender, subject, date, body.strip()
