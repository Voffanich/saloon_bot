from ast import Str
import re
import string
from typing import Dict, List
from xmlrpc.client import Boolean
import pandas as pd
from db_handler import db
from client import Client
from telebot import types


def validate_phone(phone_number: str) -> List [Boolean]:
    if re.fullmatch(r'[+]?375(29|33|44|25)\d{7}\b', phone_number):
        
        if phone_number[0] != "+" and len(phone_number) == 12:
            phone_number = "+" + phone_number
        
        return [True, phone_number]
    else:
        return [False, None]
    
def validate_name(name: str) -> List [Boolean]:
    if re.fullmatch(r'\b[а-яА-Я]{2,10}\b[ ]\b[а-яА-Я]{2,12}\b', name):
        
        name = string.capwords(name).split(' ')
        first_name = name[0]
        last_name = name[1]
        return [True, first_name, last_name]
    else:
        return [False, None, None]

  
def get_procedures_excel() -> List[Str]:
    cols = [0]
    procedures_list = []
    
    procedures = pd.read_excel('user_data/procedures.xlsx', usecols=cols)['Процедура']
    
    for procedure in procedures:
        procedures_list.append(procedure)
        
    return procedures_list

def create_client_objects_from_db() -> Dict:
    client_objects = {}
    clients_data = db.get_clients_data()
    
    client_objects = {row[0]: Client(row[0], row[1], row[2], row[3], row[5], row[4] )for row in clients_data}
    
    return client_objects

def create_dates_keyboard(bot, message):
    days = ['Понедельник, 25 мая', 'Вторник, 26 мая', 'Среда, 27 мая', 'Четверг, 28 мая']
    dates = {
        'Пн, 25 мая': ['10:00', '12:00', '18:00'],
        'Вт, 26 мая': ['12:00', '16:00'],
        'Ср, 27 мая': ['10:00', '12:00', '14:00', '16:00'],
        'Чт, 28 мая': ['10:00', '12:00', '14:00', '16:00', '18:00'],
        'Пт, 29 мая': ['10:00', '16:00'],
        'Сб, 30 мая': ['10:00', '12:00', '14:00', '16:00'],
        'Вс, 31 мая': ['10:00'],
        'Пн, 1 июня': ['10:00', '12:00', '16:00'],
        'Вт, 2 июня': ['10:00', '12:00', '14:00', '16:00'],
        'Ср, 3 июня': ['14:00', '16:00'],
        'Чт, 4 июня': ['10:00', '14:00', '16:00']        
    }
    
    btns = []
    
    for day, times in dates.items():
        dates_keyboard = types.InlineKeyboardMarkup(row_width=3)
        btns.append(types.InlineKeyboardButton(day + ' (' + str(len(times)) + ')', callback_data= day))
    
    btns.append(types.InlineKeyboardButton('Выбор процедуры', callback_data='choose_procedure'))    
    proc_slice = slice(0, len(btns)-1, 1)
    dates_keyboard.add(*btns[proc_slice])
    dates_keyboard.row(btns[-1])              
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите день', reply_markup=dates_keyboard)
    