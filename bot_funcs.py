import json
import re
import string
import time
from typing import Dict, List
from unicodedata import name
from xmlrpc.client import Boolean
from zoneinfo import available_timezones
from matplotlib.style import available
import pandas as pd
from db_handler import db
from client import Client
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import schedule
import ru_dates as rd

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

def get_available_times(procedure: str, days_in_future: int = 30) -> dict:
    available_time_windows = {}
    
    procedures = db.get_procedures_data()
    
    for proc in procedures:
        if proc['procedure'] == procedure:
            procedure_duration = timedelta(hours = int(proc['duration'].split(':')[0]), minutes = int(proc['duration'].split(':')[1])) # format '00:00:00'
            
    procedure_timetable = db.get_procedure_timetable(procedure) # {'Mon': '0', 'Tue': '10:00-13:00', 'Wed': '0', 'Thu': '10:00-13:00', 'Fri': '0', 'Sat': '0', 'Sun': '0'}
    
    for i in range(0, days_in_future-1):
        day_windows = []
        day = date.today()
        day_shift = timedelta(days = i)
        
        # creating date as 'Вт, 5 июля'
        ru_day = rd.ru_weekday_comma_date(day + day_shift)
        
        available_time = procedure_timetable[dt.strftime(day + day_shift, '%a')]
        
        if available_time != '0':
            time_shift = timedelta(0)
            time_start = available_time.split('-')[0]
            time_finish = available_time.split('-')[1]
            period_start = dt.strptime(f'{str(day + day_shift)} {time_start}', '%Y-%m-%d %H:%M')
            period_finish = dt.strptime(f'{str(day + day_shift)} {time_finish}', '%Y-%m-%d %H:%M')
            
            time_left = period_finish - period_start
            
            while time_left > procedure_duration:
                
                window = dt.strftime(period_start + time_shift, '%H:%M')
                day_windows.append(window)
                
                time_shift += procedure_duration
                time_left = period_finish - period_start - time_shift
            
            available_time_windows[ru_day] = day_windows
            # print(available_time_windows)   
            
    return available_time_windows 

