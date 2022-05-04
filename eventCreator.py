from __future__ import print_function
import datetime
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


lazyTaskDat = 'Tracker'+os.sep+'lazyTaskUpdate.txt'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # print(calendar_list_entry['id'])
            # Call the Calendar API

            # print(calendar_list_entry['summary'] == "Z LOG")
            if calendar_list_entry['summary'] == "Z Daily Life $T":

                f = open(lazyTaskDat, "r")
                # print("f:",f.read())
                fread = f.read().replace("  \n", "")
                fread = fread.replace(' ', ',', 1)
                # dont forget to repladce time format " \n"
                arguments = fread.split(',')
                targetTime = datetime.datetime.utcnow(
                )-datetime.timedelta(int(arguments[0]))
                targetTimeFormatted = targetTime.date().isoformat()  # 'Z' indicates UTC time

                category = ''
                summaryPreq = ""
                summaryPost = ""
                mid = ""

                if 0 < int(arguments[0]) < 10:
                    summaryPreq += "0"
                if int(arguments[0]) != 0:
                    summaryPreq += arguments[0]
                    summaryPost = " zzz"
                    mid += " "
                mid += arguments[1]

                summary = summaryPreq+mid+summaryPost

                id = calendar_list_entry['id']
                event = {}
                event['summary'] = summary

                event['start'] = {
                    'date': targetTimeFormatted,
                    'timeZone': 'America/Los_Angeles',
                }
                event['end'] = {
                    'date': targetTimeFormatted,
                    'timeZone': 'America/Los_Angeles',
                }
                # if category:
                # event['description']=category
                print(str(event)+"AAAA")
                event = service.events().insert(calendarId=id, body=event).execute()

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    main()
