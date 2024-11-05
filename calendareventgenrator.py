import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Path to your OAuth 2.0 client credentials file
CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Perform the OAuth 2.0 authorization flow
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)  # Opens a local server for OAuth authentication

# Initialize the Google Calendar API service
service = build('calendar', 'v3', credentials=creds)

def create_event(summary, start_date_str, end_date_str, description):
    # Set default time to 00:00 (midnight)
    default_time = "00:00"

    # Combine date and default time
    start_time_str = f"{start_date_str} {default_time}"
    end_time_str = f"{end_date_str} {default_time}"

    # Parse start and end times to datetime objects
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    # Print the parsed times for debugging
    print(f"Start Time: {start_time.isoformat()}")
    print(f"End Time: {end_time.isoformat()}")

    # Check that end time is after start time
    if end_time <= start_time:
        raise ValueError("End time must be after start time.")

    # Define the event details
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',  # Adjust as needed
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
    }

    # Insert the event into the calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

# Input details for the event
summary = input("Enter the event summary: ")
start_date_str = input("Enter the start date (YYYY-MM-DD): ")
end_date_str = input("Enter the end date (YYYY-MM-DD): ")
description = input("Enter a description for the event: ")

# Create the event
create_event(summary, start_date_str, end_date_str, description)
