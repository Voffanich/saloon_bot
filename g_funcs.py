import pprint
from googleapiclient.discovery import build
from google.oauth2 import service_account

class Google_calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH ='user_data\saloon-bot-34fbbe2b1782.json'
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename = self.FILE_PATH, scopes = self.SCOPES)
        self.service = build('calendar', 'v3', credentials = credentials)
        
    def get_calendar_list(self):
        return self.sevice.calendar_list().list().execute()

obj = Google_calendar()


pprint.pprint(obj.get_calendar_list())