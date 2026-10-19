---
name: google-workspace
description: Reaching the user's own Gmail, Calendar, Drive and Sheets from the terminal through official Google APIs and tools.
---
# Google Workspace from the terminal

Only touch the account the user is signed in with. Never read, send or share anything on someone else's behalf, and never ask for another person's password.

**Quickest wins, no setup**
- A Sheet as CSV: if it is shared by link, `curl -L "https://docs.google.com/spreadsheets/d/<ID>/export?format=csv&gid=0" -o sheet.csv`. The ID is in the URL; `gid` is the tab. Private sheets return a login page, so use the API below.
- Docs and Slides export the same way: `/document/d/<ID>/export?format=pdf` or `format=docx`.
- Calendar: ask the user for the private iCal address in Calendar settings and `curl` it, or read it with `khal`.

**Official APIs with OAuth**
1. Create a project at console.cloud.google.com, enable Gmail, Calendar, Drive or Sheets API, then create an OAuth client of type Desktop app and download `credentials.json`. Ask the user to do this in the browser.
2. `pip install google-api-python-client google-auth-oauthlib`.
3. Run the consent flow once. Request the smallest scopes, such as `https://www.googleapis.com/auth/gmail.readonly`, `calendar.readonly`, `drive.readonly`, `spreadsheets`.
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)   # opens the browser
svc = build("sheets", "v4", credentials=creds)
rows = svc.spreadsheets().values().get(spreadsheetId=ID, range="Sheet1!A1:D50").execute()
```
4. Save the token in `~/.config/gworkspace/token.json` with `chmod 600`. Never commit `credentials.json` or the token.

**CLI tools**
- `gcloud auth login` handles Google Cloud only, not mail or Drive content.
- `gam` is for Workspace admins managing a domain. Do not use it unless the user is an admin and asked.
- `rclone config` (type drive) mounts or copies Drive files.

**Habits**
- Start read-only. Ask before any write, send or delete, and show the exact change first.
- Print counts and subject lines, not full private message bodies, unless asked.
- If a call returns 403, the scope or API is not enabled. Fix that, do not work around it.
