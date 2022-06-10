import re
import string
from typing import Dict, List
from unicodedata import name
from xmlrpc.client import Boolean
import pandas as pd
from db_handler import db
from client import Client


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