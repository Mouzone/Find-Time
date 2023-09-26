from __future__ import print_function

import datetime
import os.path
import TimeGapCalculator


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from timespan import Timespan

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        timespan_list = []
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        dueDate = (datetime.datetime.utcnow() + datetime.timedelta(days=8)).isoformat() + 'Z'
        # when days = 1 it goes exactly 24hrs

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=dueDate, singleEvents=True,
                                              orderBy='startTime').execute()
        # timeMax is the latest start time
        # timeZone
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            timespan_list.append(Timespan(True, start, end))
            print(start, end, event['summary'])

        timespans = TimeGapCalculator.overlap_calculator(timespan_list)
        free_timespans = TimeGapCalculator.freetime_calculator(timespans, dueDate)

        for i in timespans:
            i.print_timespan()

        print("Free Timespans:")
        for i in free_timespans:

            i.print_timespan()
            print("\n")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
