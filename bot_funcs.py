import json
import re
import string
import time
from typing import Dict, List
from xmlrpc.client import Boolean
import pandas as pd
from db_handler import db
from client import Client
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import schedule
import ru_dates as rd
import portion as p

def validate_phone(phone_number: str) -> List [Boolean]:
    if re.fullmatch(r'[+]?375(29|33|44|25)\d{7}\b', phone_number):
        
        if phone_number[0] != "+" and len(phone_number) == 12:
            phone_number = "+" + phone_number
        
        return [True, phone_number]
    else:
        return [False, None]
    
def validate_name(name: str) -> list [Boolean]:
    if re.fullmatch(r'\b[а-яА-Я]{1,10}\b[ ]\b[а-яА-Я]{1,12}\b', name):
        
        name = string.capwords(name).split(' ')
        first_name = name[0]
        last_name = name[1]
        return [True, first_name, last_name]
    else:
        return [False, None, None]

  
def get_procedures_excel() -> list[str]:
    cols = [0]
    procedures_list = []
    
    procedures = pd.read_excel('user_data/procedures.xlsx', usecols=cols)['Процедура']
    
    for procedure in procedures:
        procedures_list.append(procedure)
        
    return procedures_list

def create_client_objects_from_db() -> dict:
    client_objects = {}
    clients_data = db.get_clients_data()
    
    client_objects = {row[0]: Client(row[0], row[1], row[2], row[3], row[5], row[4] )for row in clients_data}
    
    return client_objects

def procedure_name_from_id(procedures: list, id: int) -> str:
    """Returns procedure name from database according to provided id

    Args:
        procedures (list): list of procedures with dictionaries with procedures parameters (copy of database table)
        id (int): provided id of the procedure which name is needed

    Returns:
        str: name of the procedure by it's id from database
    """
    name_found = False
    
    for procedure in procedures:
        if procedure['id'] == id:
            name = procedure['procedure']
            name_found = True

    if name_found:
        return name
    else:
        return 'No such procedure id in database'
    
def procedure_id_from_name(procedures: list, procedure_name: str) -> int:
    """Returns procedure id from database according to provided procedure name

    Args:
        procedures (list): list of procedures with dictionaries with procedures parameters (copy of database table)
        name (str): provided name of the procedure which id is needed

    Returns:
        int: id of the procedure by it's name from database
    """
    id_found = False
    
    for procedure in procedures:
        if procedure['procedure'] == procedure_name:
            id = procedure['id']
            id_found = True

    if id_found:
        return id
    else:
        return 'No such procedure name in database'

# NOT USED??
def procedure_duration_from_id(procedures: list, id: int) -> str:
    """Returns procedure duration from database according to provided id

    Args:
        procedures (list): list of procedures with dictionaries with procedures parameters (copy of database table)
        id (int): provided id of the procedure which name is needed

    Returns:
        str: duration of the procedure by it's id from database
    """
    duration_found = False
    
    for procedure in procedures:
        if procedure['id'] == id:
            duration = procedure['duration']
            duration_found = True

    if duration_found:
        return duration
    else:
        return 'No such procedure id in database'
    
# a crutch that helps to avoid an error of unknown id that appears on bot startup
def check_flag(clients: dict, id: int) -> str:
    if id in clients:
        if clients[id].flag == 'проверить телефон':
            return 'проверить телефон'
        elif clients[id].flag == 'проверить имя':
            return 'проверить имя'
        else:
            return False
    else:
        return 'Id not found in database'

# function for asyncronous scheduled tasks of the bot, like backups, messaging, reminders   
def scheduled_tasks(db_file_name: str, days_to_store_backups: int):
    # db file backup every day
    schedule.every().day.at('02:00').do(db.backup_db_file, db_file_name, 'daily')
    # delete files of db backups older than days_to_store_backups
    schedule.every().day.at('02:00').do(db.clear_old_db_backups, days_to_store_backups, 'backups')
    while True:
        schedule.run_pending()
        time.sleep(10)
        
def read_config(file_name: str) -> dict:
    with open(file_name) as config_file:
        config = json.load(config_file)
    return config

def get_available_times(procedures: dict, procedure_id: int, days_in_future: int = 30, minute_time_gap: int = 30) -> dict:
    available_time_windows = {}
    time_gap = timedelta(0)
    
    procedure_duration = timedelta(hours = int(procedures[procedure_id - 1]['duration'].split(':')[0]), 
                                   minutes = int(procedures[procedure_id - 1]['duration'].split(':')[1])) # format '00:00:00'
    procedure_timetable = db.get_procedure_timetable(procedure_id) # {'Mon': '0', 'Tue': '10:00-13:00', 'Wed': '0', 'Thu': '10:00-13:00', 'Fri': '0', 'Sat': '0', 'Sun': '0'}
    
    # getting occupied time periods as Portion lib objects for chosen procedure for X days in the future
    occupied_periods = db.get_occupied_periods(days_in_future)
    
    for i in range(0, days_in_future):
        day_windows = []
        day = date.today()
        day_shift = timedelta(days = i)        
        
        if i == 0:
            time_gap = timedelta(minutes = minute_time_gap)
        
        # creating date as 'Вт, 5 июля'
        ru_day = rd.ru_weekday_comma_date(day + day_shift)
          
        # available time period for booking of current procedure ('10:00-13:00') %a - a weekday name in format Mon, Tue, etc.
        available_day_period = procedure_timetable[dt.strftime(day + day_shift, '%a')]
        
        if available_day_period != '0':
            time_shift = timedelta(0)
            # time adjustment is used for adjusting time shift in case when estimated window intersects the occupied period from bottom
            # and the upper bound of the window is withing occupied period or above the upper bound of occupied period
            time_adjustment = timedelta(0)
            
            day_period_start = available_day_period.split('-')[0]
            day_period_finish = available_day_period.split('-')[1]
            
            # available day period as portion lib object
            available_period = p.closed(dt.strptime(str(day + day_shift) + day_period_start, '%Y-%m-%d%H:%M'), dt.strptime(str(day + day_shift) + day_period_finish, '%Y-%m-%d%H:%M'))
            
            time_left = available_period.upper - available_period.lower
            print(f'time_left beginning of day: {time_left}')
            
            while time_left > procedure_duration:
                
                window = p.open(available_period.lower + time_shift, available_period.lower + time_shift + procedure_duration)
                print(f'window: {dt.strftime(window.lower, "%Y-%m-%d %H:%M")} - {dt.strftime(window.upper, "%H:%M")}')      
                print(f'time shift - {time_shift}')
                print(f'procedure duration {procedure_duration}')
                
                window_occupied = False
                
                for occupied_period in occupied_periods:
                    if not window < occupied_period and not window > occupied_period:
                        window_occupied = True
                        print(f'{window_occupied=}')
                        time_adjustment = occupied_period.upper - window.upper
                        
                time_shift += procedure_duration + time_adjustment
                time_left -= procedure_duration + time_adjustment
                
                print(f'time shift 2 {time_shift}')
                print(f'time left {time_left}')
                            
                if not window_occupied and window.lower > dt.now() + time_gap:
                    day_windows.append(dt.strftime(window.lower, '%H:%M'))
                    
                    
            print(ru_day, day_windows, '\n')
            
            if len(day_windows) > 0:
                available_time_windows[ru_day] = day_windows
            
    return available_time_windows
    
def window_occupied(booked_date, procedure_duration, days_in_future) -> bool:
    window_occupied = False
    duration = timedelta(hours = int(procedure_duration.split(':')[0]), minutes = int(procedure_duration.split(':')[1]))
    window = p.open(booked_date, booked_date + duration)
    
    occupied_periods = db.get_occupied_periods(days_in_future)
                
    for occupied_period in occupied_periods:
        if not window < occupied_period and not window > occupied_period:
            window_occupied = True
            
    return window_occupied