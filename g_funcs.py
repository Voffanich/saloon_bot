import calendar
import datetime
import pprint
import re
import time
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

import ru_dates as rd
import portion as p
from db_handler import db


class Google_calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    user_data_path = Path('user_data/')
    FILE_PATH = user_data_path / 'g_config.json'
    
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
                            filename = self.FILE_PATH, scopes = self.SCOPES)
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
        
        # print(days_in_month[-1])
        
        
        # adding 0 to month num in the beginning if month num is 1 to 9
        if month_num < 10:
            month_str = '0' + str(month_num)
        else: 
            month_str = str(month_num)
            
        # preparing time range start and finish in required format for calendar API        
        time_min = f'{dt.now().year + year_shift}-{month_str}-01T00:00:00+03:00'
        time_max = f'{dt.now().year + year_shift}-{month_str}-{days_in_month[-1]}T23:59:59+03:00'
        
        # print(f'{time_max=}')
        # print(f'{time_min=}')
        
        # getting events from calendar from the range between time_min and time_max
        # siingleEvents shows copies of the repeating event, not only inital event
        events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                           timeMax = time_max, singleEvents = True).execute()
        
        # for event in events:
        #     print(event, '\n')
        
        windows_count = 0
        
        for item in events['items']:
            if 'summary' in item:
                if 'окно' in item['summary'].lower():
                    windows_count += 1 
                    # getting start time of window in format '2023-01-08T14:20:00'
                    windows.append(item['start']['dateTime'].split('+')[0])
                    # getting start time of window in datetime format
                    windows_time_format.append(dt.strptime(item['start']['dateTime']
                                                .split('+')[0], '%Y-%m-%dT%H:%M:%S'))
        
        windows_time_format.sort()
        
        for date in windows_time_format:
            day = dt.strftime(date, '%d.%m') + f' ({rd.ru_d_short(date)})'
            time = dt.strftime(date, '%H:%M')
            if day in windows_dict:
                windows_dict[day].append(time)
            else:
                windows_dict[day] = [time]
        
        message_text = ''
        
        for day, times in windows_dict.items():
            date_line = day + ': '
            for time in times:
                date_line = date_line + time + ', '
                
            print(date_line[:-2])
            message_text += date_line[:-2]
            message_text += '\n' 
        # print(message_text)
        
        if not message_text:
            message_text = "В выбранно месяце свободных для записи окон нет."
                
        return message_text
    
    def get_available_times(self, calendar_id, days_ahead: int, mins_to_nearest_book: int) -> dict:
        
        windows = []
        windows_time_format = []
        windows_dict = {}  
        
        period_start_time = dt.now() + timedelta(minutes=mins_to_nearest_book)
        period_finish_time = dt.now() + timedelta(days=days_ahead)
        
        time_min = dt.strftime(period_start_time, '%Y-%m-%dT%H:%M:00+03:00')
        time_max = dt.strftime(period_finish_time, '%Y-%m-%dT%H:%M:00+03:00')
        
        print(f'{time_min=}\n{time_max=}')
        
         # preparing time range start and finish in required format for calendar API        
        
                
        # getting events from calendar from the range between time_min and time_max
        # siingleEvents shows copies of the repeating event, not only inital event
        events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                           timeMax = time_max, singleEvents = True).execute()
        
        for item in events['items']:
            if 'summary' in item:
                if 'окно' in item['summary'].lower():
                    # windows.append(item['start']['dateTime'].split('+')[0])
                    # getting start time of window in datetime format
                    windows_time_format.append(dt.strptime(item['start']['dateTime']
                                                .split('+')[0], '%Y-%m-%dT%H:%M:%S'))

        windows_time_format.sort()
                    
        # print(f'{windows_time_format=}')
        
        for date in windows_time_format:
            day = dt.strftime(date, '%d.%m') + f', {rd.ru_d_short(date)}'
            time = dt.strftime(date, '%H:%M')
            if day in windows_dict:
                windows_dict[day].append(time)
            else:
                windows_dict[day] = [time]
                
        # print(f'{windows_dict=}')
        
        return windows_dict
        
    
    def occupy_window(self, calendar_id, start_time, telegram_id) -> bool:
        
        time_min = dt.strftime(start_time, '%Y-%m-%dT%H:%M:%S+03:00')
        time_max = dt.strftime(start_time + timedelta(hours=12), '%Y-%m-%dT%H:%M:%S+03:00')
        
        try:
            events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                           timeMax = time_max, singleEvents = True).execute()
            for event in events['items']:
                if event['start']['dateTime'] == time_min and event['summary'].lower() == 'окно':
                    window = event
                
        except Exception as ex:
            print(f'Some fucking error happened')
            print(ex)
            return False
            
        window['summary'] = f'Бронь с {dt.strftime(dt.now(),"%Y-%m-%d %H:%M")}'
        window['description'] = telegram_id
                
        
        occupied_window = self.service.events().update(calendarId=calendar_id, eventId=window['id'], body=window).execute()
        
        print(f'Window occupied \n {occupied_window["summary"]}')
        
        return True
                    
                    
                       
    def check_window_occupation(self, calendar_id, start_time, telegram_id) -> bool:
        
        time_min = dt.strftime(start_time, '%Y-%m-%dT%H:%M:%S+03:00')
        time_max = dt.strftime(start_time + timedelta(hours=12), '%Y-%m-%dT%H:%M:%S+03:00')
        
        try:
            events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                           timeMax = time_max, singleEvents = True).execute()
            
            for event in events['items']:
                if event['start']['dateTime'] == time_min: 
                    # print('CWO window found')
                    window = event
                    
                    # print(f'CWO {window["description"]=}\n{telegram_id}')
                    
                    if 'бронь' in event['summary'].lower() and int(window['description']) == telegram_id:
                        # print(f'CWO check 1')
                        return True
                    elif 'окно' in event['summary'].lower():
                        # print(f'CWO check 2')
                        return True
                    else:
                        # print(f'CWO check 3')
                        return False
                
        except Exception as ex:
            print(f'Some fucking error happened')
            print(ex)
            return False
        
        
    
    
    def add_visit(self, calendar_id, booked_date, telegram_id, procedure_id, client_name, price) -> bool:
        
        time_min = dt.strftime(booked_date, '%Y-%m-%dT%H:%M:%S+03:00')
        time_max = dt.strftime(booked_date + timedelta(hours=12), '%Y-%m-%dT%H:%M:%S+03:00')
        
        try:
            events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                           timeMax = time_max, singleEvents = True).execute()
            for event in events['items']:
                if event['start']['dateTime'] == time_min: 
                    print('AV window found')
                    window = event
                    
                    if 'бронь' in event['summary'].lower() and int(window['description']) == telegram_id or 'окно' in event['summary'].lower():
                        window['summary'] = client_name + f' {price}'
                        window['description'] = db.procedure_name_from_id(procedure_id) + '\ntg'   

                        occupied_window = self.service.events().update(calendarId=calendar_id, eventId=window['id'], body=window).execute()
                        
                        print(f'Window filled with visit \n {occupied_window["summary"]=}\n{occupied_window["description"]=}')
                    
                        
        except Exception as ex:
            print(f'Some fucking error happened')
            print(ex)
            return False   
    
    
    def reset_occupations(self, calendar_id, days_to_show_windows, mins_to_occupy_window) -> bool:
        time_min = dt.strftime(dt.now() - timedelta(minutes=mins_to_occupy_window + 10), '%Y-%m-%dT%H:%M:%S+03:00')
        time_max = dt.strftime(dt.now() + timedelta(days=days_to_show_windows), '%Y-%m-%dT%H:%M:%S+03:00')
        
        try:
            events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, 
                                        timeMax = time_max, singleEvents = True).execute()
            
            if events:
                for event in events['items']:
                    
                    if 'summary' in event and 'бронь' in event['summary'].lower():
                        occupation_time = dt.strptime(event['summary'].split(' ')[2] + event['summary'].split(' ')[3], "%Y-%m-%d%H:%M")                  
                        print(f'RO {occupation_time=}')
                        
                        if occupation_time < dt.now() - timedelta(minutes=mins_to_occupy_window):
                            event['summary'] = 'Окно'
                            event['description'] = ''
                            
                            occupied_window = self.service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()
                            
                            print(f'RO window reset to unoccupied {occupied_window["start"]["dateTime"]}')  
                            
                            return True
            else:
                print('No occupied windows found')    
                
        except Exception as ex:
            print(f'Some fucking error happened')
            print(ex)
            return False  
            
    
    def show_stats(self, calendar_id, month_shift: int):
        
        month_num = int(dt.strftime(dt.now(), "%m")) + month_shift
        
        if month_num > 12:
            month_num = month_num - 12
            year = str(int(dt.strftime(dt.now(), "%Y")) + 1)
            print(f'{year=} {month_num=}')
        elif month_num < 1:
            month_num = month_num + 12
            year = str(int(dt.strftime(dt.now(), "%Y")) - 1)
            print(f'{year=} {month_num=}')
        else:
            year = dt.strftime(dt.now(), "%Y")
            print(f'{year=} {month_num=}')
            
        ru_month_name = rd.ru_m_full(month_num=month_num)
        
        days_in_month = calendar.monthrange(dt.now().year, month_num)
        
        #print(days_in_month[-1])
        
        time_min = f'{year}-{"0" if month_num < 10 else ""}{month_num}-01T00:00:00+03:00'
        time_max = f'{year}-{"0" if month_num < 10 else ""}{month_num}-{days_in_month[-1]}T23:59:59+03:00'
        
        # Check time_max and time_min format
        print(f'time_min={time_min}')
        print(f'time_max={time_max}')
        
        # '2022-12-01T00:00:00+03:00'
        
        events = self.service.events().list(calendarId=calendar_id, timeMin = time_min, timeMax = time_max, singleEvents = True).execute()
        
        manicure = 0
        pedicure = 0
        windows = 0
        
        manicure_stats = {'total_count': 0, 'priced_count': 0, 'sum': 0}
        pedicure_stats = {'total_count': 0, 'priced_count': 0, 'sum': 0}
        
        for item in events['items']:
           
            if 'summary' in item:
                # print(item['summary'])    
                if 'окно' in item['summary'].lower() and dt.strptime(item['start']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S') > dt.now():
                    # print(item['summary'], item['start'], item['end'])
                    windows += 1    
            # else: 
                # print('No summary')
            if 'description' in item:
                # print(item['description'])
                if 'маникюр' in item['description'].lower():
                    manicure += 1
                    
                    if dt.strptime(item['end']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S') < dt.now() and 'summary' in item:   
                        # считаем все визиты с чеком или без
                        manicure_stats['total_count'] += 1  
                        
                        check = re.findall(r'\b\d{1,3}\b', item['summary'])
                        print(check)
                        if check:
                            # считаем визиты с чеком и итоговую сумму
                            manicure_stats['priced_count'] += 1
                            manicure_stats['sum'] += int(check[0])
                        
                        
                if 'педикюр' in item['description'].lower():
                    pedicure += 1
                    
                    if dt.strptime(item['end']['dateTime'].split('+')[0], '%Y-%m-%dT%H:%M:%S') < dt.now() and 'summary' in item:       
                        # считаем все визиты с чеком или без
                        pedicure_stats['total_count'] += 1  
                         
                        check = re.findall(r'\b\d{1,3}\b', item['summary'])
                        print(check)
                        if check:
                            pedicure_stats['priced_count'] += 1
                            pedicure_stats['sum'] += int(check[0])
            # else: 
            #     print('No description')
            # if 'colorId' in item:
            #     print(item['colorId'])
            # else: 
            #     print('No colorId')
            # print('   ')
        
        print(f'{manicure_stats["total_count"]=}, {manicure_stats["priced_count"]=}, {manicure_stats["sum"]=} ')
        print(f'{pedicure_stats["total_count"]=}, {pedicure_stats["priced_count"]=}, {pedicure_stats["sum"]=} ')
        
        manicure_price = 58
        pedicure_price = 58
        
        if manicure_stats['total_count'] > 0:
            if manicure_stats['priced_count'] > 0:
                average_manicure_check = manicure_stats['sum'] / manicure_stats['priced_count']
            else: 
                average_manicure_check = manicure_price
        else:
            average_manicure_check = 0
        blanc_manicure_sum = ((manicure_stats['total_count'] - manicure_stats['priced_count'])) * manicure_price
           
        
        if pedicure_stats['total_count'] > 0:
            if pedicure_stats['priced_count'] > 0:
                average_pedicure_check = pedicure_stats['sum'] / pedicure_stats['priced_count']
            else:
                average_pedicure_check = pedicure_price
        else:
            average_pedicure_check = 0
        blanc_pedicure_sum = ((pedicure_stats['total_count'] - pedicure_stats['priced_count'])) * pedicure_price   
            
           
        total_income = manicure_stats['sum'] + pedicure_stats['sum'] + blanc_manicure_sum + blanc_pedicure_sum
        
        try:
            # print('we are here 1') 
            message_text = f"""
    Статистика за <b>{ru_month_name.capitalize()}</b>        

    Оценка заработка за весь месяц:        

    Маникюр: <b>{manicure}</b> визитов х {manicure_price} р.
    Педикюр: <b>{pedicure}</b> визитов х {pedicure_price} р.
    Доход со всех <b>{manicure + pedicure}</b> визитов <b>{manicure*manicure_price + pedicure*pedicure_price} р.</b>
    """
            # статистика по фактическому заработку только для текущего и предыдущих месяцев при наличии завершенных визитов
            if month_shift < 1:
                # проверка на наличие завершенных визитов
                if manicure_stats['total_count'] > 0 or pedicure_stats['total_count'] > 0:
                        message_text += f"""
    Фактический заработок на данный момент:

    Средний чек за маникюр: <b>{round(average_manicure_check, 2)} р.</b> (процедур: {manicure_stats["total_count"]})
    Средний чек за педикюр: <b>{round(average_pedicure_check, 2)} р.</b> (процедур: {pedicure_stats["total_count"]})
    Всего заработано: <b>{round(total_income, 2)} р.</b>
            """
            message_text += f"""
    Свободных окон до конца месяца - {windows}
            """
        except Exception as ex:
            print(ex)
            
        print(message_text)
        
        return message_text
        # return total_bookings, remained_bookings
    
    
    def place_windows(self, calendar_id: str, window_duration: str, mode: str, days_off: list, work_day_start: str, work_day_finish: str, period_start: str, period_finish: str,
                      events_gap: int, events_shift: int):
        
        color_code = 10     # basilic in google calendar (dark green)
        # windows = [p.open(dt.strptime('2024-04-04 10:00:00', '%Y-%m-%d %H:%M:%S'), dt.strptime('2024-04-04 10:30:00', '%Y-%m-%d %H:%M:%S'))]
        windows = []
        
        time_min = f'{period_start}T00:00:00+03:00'
        time_max = f'{period_finish}T23:59:59+03:00'
        
        try:
            events_result = self.service.events().list(calendarId=calendar_id, timeMin = time_min, timeMax = time_max, fields = 'items(id,summary,start,end,description)',
                                            orderBy = 'startTime', singleEvents = True).execute()       
        except Exception as ex:
            print(ex)
            
        existing_events = events_result.get('items', [])
        
        time_min_dt = dt.strptime(time_min, '%Y-%m-%dT%H:%M:%S+03:00')
        time_max_dt = dt.strptime(time_max, '%Y-%m-%dT%H:%M:%S+03:00')
        
        days_to_place_windows = (time_max_dt - time_min_dt).days + 1    # getting the nubmer of days to place windows including start date and finish date days
        
        date = time_min_dt
        work_events = []
        other_events = []
        events_frames = {'work':[], 'other':[]}
        
        while True:
            if date.day not in days_off:
                print(f'{date=}')
                
                for event in existing_events:
                    if dt.fromisoformat(event['start']['dateTime']).date() == date.date():
                        print(f'Event found')
                        print(event)
                        if 'description' in event and 'маникюр' in event['description'].lower() or 'description' in event and 'педикюр' in event['description'].lower() or 'summary' in event  and 'окно' in event['summary'].lower():
                            events_frames['work'].append(p.open(dt.fromisoformat(event['start']['dateTime']), dt.fromisoformat(event['end']['dateTime'])))
                            work_events.append(p.open(dt.fromisoformat(event['start']['dateTime']), dt.fromisoformat(event['end']['dateTime'])))
                        else:
                            events_frames['other'].append(p.open(dt.fromisoformat(event['start']['dateTime']), dt.fromisoformat(event['end']['dateTime'])))
                            other_events.append(p.open(dt.fromisoformat(event['start']['dateTime']), dt.fromisoformat(event['end']['dateTime']))) 
                
                all_events: list = (work_events + other_events)
                all_events.sort()
                print(f'{all_events=}')
                        
                if not all_events:
                    print('No existing events')
                    current_time = date + timedelta(hours=int(work_day_start.split(':')[0]), minutes=int(work_day_start.split(':')[1]))    
                    window_length = timedelta(hours=int(window_duration.split(':')[0]), minutes=int(window_duration.split(':')[1]))  
                    day_finish_time = date + timedelta(hours=int(work_day_finish.split(':')[0]), minutes=int(work_day_finish.split(':')[1]))  
                    events_shift_time = timedelta(minutes=events_shift)  
                        
                    while True:
                        print(current_time)
                        windows.append(p.open(current_time, current_time + window_length))
                        current_time += window_length
                        
                        if current_time + window_length - day_finish_time > events_shift_time:
                            break
                else:    
                    pass
                        
                        
            
            date += timedelta(days=1)
            events_frames = {'work':[], 'other':[]}
            all_events = []
            work_events = []
            other_events = []
            
            if date > time_max_dt:
                break
        

        if windows:
            for window in windows:
                window_start_time = dt.strftime(window.lower, '%Y-%m-%dT%H:%M:%S+03:00')
                window_finish_time = dt.strftime(window.upper, '%Y-%m-%dT%H:%M:%S+03:00')
                
                window_event = {
                'summary': f'Окно',
                # 'location': 'Минск',
                'description': '',
                'start': {
                    'dateTime': f'{window_start_time}',
                    'timeZone': 'Europe/Minsk' 
                },
                'end': {
                    'dateTime': f'{window_finish_time}',
                    'timeZone': 'Europe/Minsk' 
                },      
                'colorId':f'{color_code}'                 
                } 

                try:
                    event = clndr.add_event(calendar_id=calendar_id, event=window_event)
                    
                except Exception as ex:
                    print(ex)
                
                time.sleep(0.5)    
            
        
        

clndr = Google_calendar()
calendar_id_1 = 'voffanich@gmail.com'
calendar_id_2 = 'kazlova.alesia@gmail.com'

# clndr.add_calendar('kazlova.alesia@gmail.com')

# pprint.pprint(clndr.get_calendar_list())

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

# event = clndr.add_event(calendar_id=calendar_id, event=event)

# events = clndr.service.events().list(calendarId=calendar_id_2, timeMin = '2022-11-01T00:00:00+03:00', timeMax = '2022-11-30T23:59:00+03:00').execute()
# events = clndr.service.events().list(calendarId=calendar_id_2, timeMin = '2022-12-01T00:00:00+03:00', timeMax = '2022-12-31T23:59:00+03:00').execute()

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


# clndr.show_stats(calendar_id=calendar_id_2, month_shift=0)

# windows = clndr.show_windows(calendar_id=calendar_id_2, month_shift=0)

# for day, times in windows.items():
#     date_line = day + ': '
#     for time in times:
#         date_line = date_line + time + ', '
#     print(date_line[:-2])