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
            # print("=======\n"+str(calendar_list_entry)+"=======\n")
            # print(calendar_list_entry['summary'])
            # Call the Calendar API

            # print(calendar_list_entry['summary'] == "Z LOG")
            if calendar_list_entry['summary'] == "Z Daily Life $T":

                f = open(lazyTaskDat, "r")
                # print("f:",f.read())
                fread = f.read().replace("  \n", "")
                print("fread:", fread)
                # dont forget to repladce time format " \n"
                arguments = fread.split(' ')
                print(arguments)
                targetTime = datetime.datetime.utcnow(
                )-datetime.timedelta(int(arguments[0]))
                # targetTimeFormatted = targetTime.isoformat() + 'Z'  # 'Z' indicates UTC time
                targetTimeFormatted = targetTime.date().isoformat()  # 'Z' indicates UTC time
                print(targetTime)
                print(targetTimeFormatted)

                category = ''
                summaryPreq = ""
                if int(arguments[0]) < 10:
                    summaryPreq += "0"
                summaryPreq += arguments[0]
                summary = summaryPreq+" "+arguments[1]+" zzz"
                # if len(arguments)==3:
                #     intent=arguments[0]
                #     summary=arguments[1]
                #     time=str(arguments[2])
                # elif len(arguments)==4:
                #     intent=arguments[0]
                #     summary=arguments[1]
                #     category=arguments[2]
                #     time=str(arguments[3])
                # elif len(arguments)==2:
                #     intent=arguments[0]
                #     time=str(arguments[1])
                # print("\n |"+str(intent)+"| INTENT")

                # if str(intent).lower()=="finish":
                # endSummary=''
                # if summary:
                #     endSummary=summary

                # addtime=fread
                # search=re.sub('((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<6>", addtime)
                # splitHolder=search.split(', ')
                # search=splitHolder
                # search=search[len(search)-1]
                # search=int(search)
                # print(search)
                # if search!=59:
                #     search=search+1
                #     print(search)
                # if (search >9):
                #     searchFormatted=str(search)
                # else:
                #     searchFormatted="0"+str(search)
                # print(search)
                # addedString=re.sub('((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<1>"+searchFormatted+"\g<7>", addtime)

                # if not endSummary:
                #     splitHolder[len(splitHolder)-1]=addedString.lower().replace("finish","unknown")
                #     unknownSummary=", ".join(splitHolder)
                #     addedString=unknownSummary

                id = calendar_list_entry['id']
                event = {}
                # if endSummary:
                # event['summary']=endSummary
                # else:
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
