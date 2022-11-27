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
        return self.service.calendarList().list().execute()
    
    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id            
        }

        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, event):
        
        return self.service.events().insert(calendarId=calendar_id, body=event).execute()
        # print('Event created: %s' % (event.get('htmlLink')))
    

obj = Google_calendar()
calendar_id_1 = 'voffanich@gmail.com'
calendar_id_2 = 'kazlova.alesia@gmail.com'

# obj.add_calendar('kazlova.alesia@gmail.com')

# pprint.pprint(obj.get_calendar_list())

event = {
        'summary':'Аня Дубик',
        # 'location': 'Минск',
        'description': 'маникюр',
        'start': {
            'dateTime': '2022-11-28T15:00:00Z',
            'timeZone': 'Europe/Minsk' 
        },
        'end': {
            'dateTime': '2022-11-28T16:00:00Z',
            'timeZone': 'Europe/Minsk' 
        },      
        'colorId':'7'                 
        }  

# event = obj.add_event(calendar_id=calendar_id, event=event)

events = obj.service.events().list(calendarId=calendar_id_2, timeMin = '2022-11-01T00:00:00+03:00', timeMax = '2022-11-30T00:00:00+03:00').execute()
# print(events)

# for key, value in events.items():
#         print(key, ' : ', value)
    
for item in events['items']:
    print(item)
    # print(item['summary'])
    print('   ')