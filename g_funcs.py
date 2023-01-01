import calendar
import datetime
import pprint
from datetime import datetime as dt

from google.oauth2 import service_account
from googleapiclient.discovery import build

import ru_dates as rd


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
        
    def show_windows(self, calendar_id, month_shift: int) -> list:
        
        windows = []
        windows_time_format = []
        windows_dict = {}  
        year_shift = 0
        
        #preparing month num for days_in_month in case we have current month num plus month shift bigger than 12        
        month_num = dt.now().month + month_shift
        if month_num > 12:
            month_num = month_num - 12
            year_shift = 1
        
        days_in_month = calendar.monthrange(dt.now().year, month_num)
        
        print(days_in_month[-1])
        
        
        # adding 0 to month num in the beginning if month num is 1 to 9
        if month_num < 10:
            month_str = '0' + str(month_num)
        else: 
            month_str = str(month_num)
            
        # preparing time range start and finish in required format for calendar API        
        time_min = f'{dt.now().year + year_shift}-{month_str}-01T00:00:00+03:00'
        time_max = f'{dt.now().year + year_shift}-{month_str}-{days_in_month[-1]}T23:59:59+03:00'
        
        print(f'time_max={time_max}')
        print(f'time_min={time_min}')
        
        # getting events from calendar from the range between time_min and time_max
        events = obj.service.events().list(calendarId=calendar_id, timeMin = time_min, timeMax = time_max).execute()
        
        windows_count = 0
        
        for item in events['items']:
            if 'summary' in item:
                if 'окно' in item['summary'].lower():
                    windows_count += 1 
                    # getting start time of window in format '2023-01-08T14:20:00'
                    windows.append(item['start']['dateTime'].split('+')[0])
                    # getting start time of window in datetime format
                    windows_time_format.append(dt.strptime(item['start']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S'))
        
        windows_time_format.sort()
        
        for date in windows_time_format:
            day = dt.strftime(date, '%d.%m') + f' ({rd.ru_d_short(date)})'
            time = dt.strftime(date, '%H:%M')
            if day in windows_dict:
                windows_dict[day].append(time)
            else:
                windows_dict[day] = [time]
                
        return windows_dict
    
    def show_stats(self, calendar_id, month_num: int):
        
        days_in_month = calendar.monthrange(dt.now().year, month_num)
        #print(days_in_month[-1])
        
        time_min = f'{dt.strftime(dt.now(), "%Y")}-{dt.strftime(dt.now(), "%m")}-01T00:00:00+03:00'
        time_max = f'{dt.strftime(dt.now(), "%Y")}-{dt.strftime(dt.now(), "%m")}-{days_in_month[-1]}T23:59:59+03:00'
        
        # Check time_max and time_min format
        # print(f'time_max={time_max}')
        # print(f'time_min={time_min}')
        
        # '2022-12-01T00:00:00+03:00'
        
        events = obj.service.events().list(calendarId=calendar_id, timeMin = time_min, timeMax = time_max).execute()
        
        manicure = 0
        pedicure = 0
        windows = 0
        
        for item in events['items']:
            # print(item)
            
            """if 'start' in item:
                print(item['start']['dateTime'].split('T')[0])
            else: 
                print('No start')"""
            if 'summary' in item:
                # print(item['summary'])    
                if 'окно' in item['summary'].lower():
                    windows += 1    
            # else: 
                # print('No summary')
            if 'description' in item:
                # print(item['description'])
                if 'маникюр' in item['description'].lower():
                    manicure += 1        
                if 'педикюр' in item['description'].lower():
                    pedicure += 1
            # else: 
            #     print('No description')
            # if 'colorId' in item:
            #     print(item['colorId'])
            # else: 
            #     print('No colorId')
            # print('   ')
            
        print(f'Маникюр: {manicure} визитов х 45 р.')
        print(f'Педикюр: {pedicure} визитов х 40 р.')
        print(f'Доход со всех {manicure + pedicure} визитов {manicure*45 + pedicure*40} р.')
        print('')
        print(f'Свободных окон - {windows}')
        print(f'-------------------------')
        
        return events
        # return total_bookings, remained_bookings
    

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

# events = obj.service.events().list(calendarId=calendar_id_2, timeMin = '2022-11-01T00:00:00+03:00', timeMax = '2022-11-30T23:59:00+03:00').execute()
events = obj.service.events().list(calendarId=calendar_id_2, timeMin = '2022-12-01T00:00:00+03:00', timeMax = '2022-12-31T23:59:00+03:00').execute()

# print(events)

# for key, value in events.items():
#         print(key, ' : ', value)

"""
manicure = 0
pedicure = 0
windows = 0
 
for item in events['items']:
    # print(item)
    
    if 'start' in item:
        print(item['start']['dateTime'].split('T')[0])
    else: 
        print('No start')
    if 'summary' in item:
        print(item['summary'])    
        if 'окно' in item['summary'].lower():
            windows += 1    
    else: 
        print('No summary')
    if 'description' in item:
        print(item['description'])
        if 'маникюр' in item['description'].lower():
            manicure += 1        
        if 'педикюр' in item['description'].lower():
            pedicure += 1
    else: 
        print('No description')
    if 'colorId' in item:
        print(item['colorId'])
    else: 
        print('No colorId')
    print('   ')
    
    
print(f'Маникюр: {manicure} визитов х 45 р.')
print(f'Педикюр: {pedicure} визитов х 40 р.')
print(f'Доход со всех {manicure + pedicure} визитов {manicure*45 + pedicure*40} р.')
print('')
print(f'Свободных окон - {windows}')
print(f'-------------------------')
"""
"""
     'start': {'dateTime': '2022-11-28T19:00:00+03:00', 'timeZone': 'Europe/Minsk'}, 
     'end': {'dateTime': '2022-11-28T21:00:00+03:00', 'timeZone': 'Europe/Minsk'}
     
"""

#obj.show_stats(calendar_id=calendar_id_2, month_num=9)
windows = obj.show_windows(calendar_id=calendar_id_2, month_shift=1)

for day, times in windows.items():
    date_line = day + ': '
    for time in times:
        date_line = date_line + time + ', '
    print(date_line[:-2])