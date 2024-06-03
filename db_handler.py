import copy
import os
import shutil
import sqlite3
from datetime import datetime as dt
from datetime import timedelta
from pathlib import Path
from typing import Dict, List
from xmlrpc.client import Boolean

import pandas as pd
import portion as p


class DB_handler():
    
    def __init__(self, dbname='saloon.sqlite'):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.flag = ''
        # self.connection.set_trace_callback(print)
        
    def setup(self):
        query = """CREATE TABLE IF NOT EXISTS clients (
            client_id INT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            reg_date TEXT,
            visits_counter INT,
            timing TEXT,
            last_visit TEXT,
            active TEXT,
            discount INT);
            """
        try:    
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
        query = """CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            book_date TEXT,
            visit_date TEXT,
            start_time TEXT,
            finish_time TEXT,
            procedure_id INT,
            price INT,
            status TEXT);
            """
        try:    
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
        query = """CREATE TABLE IF NOT EXISTS procedures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            procedure TEXT,
            duration TEXT,
            price TEXT,
            mon_sched TEXT,
            tue_sched TEXT,
            wed_sched TEXT,
            thu_sched TEXT,
            fri_sched TEXT,
            sat_sched TEXT,
            sun_sched TEXT);
            """
        try:    
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
    def add_client(self, client_id: str, username: str, first_name: str = '', last_name: str = '', phone_number: str = '', timing: str = '2:30', last_visit: str = '', active: str = 'true', discount: int = 0):
        visits_counter = 0
        timing = '2:30'
        
        query = f"""
        INSERT INTO clients (client_id, username, first_name, last_name, phone_number, reg_date, visits_counter, timing, last_visit, active, discount)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);        
        """
        try:    
            self.cursor.execute(query, (client_id, username, first_name, last_name, phone_number, dt.strftime(dt.now(), '%Y-%m-%d %H:%M'),
                                        visits_counter, timing, last_visit, active, discount))
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
            
    # ПЕРЕСМОТРЕТЬ ИМЕНА СТОЛБЦОВ
    def add_visit(self, client_name: str, book_date: str, visit_date: str, start_time: str, finish_time: str, procedure_id: int, status: str, price: int = 35):
        # print(client_name, date, start_time, finish_time, procedure, status, price)
        query = """
        INSERT INTO visits (client_name, book_date, visit_date, start_time, finish_time, procedure_id, price, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        """
        try:
            # self.cursor.execute(query)
            self.cursor.execute(query, (client_name, book_date, visit_date, start_time, finish_time, procedure_id, price, status, ))
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
    
    def show_visits(self) -> list:
        reply = self.cursor.execute("SELECT * FROM visits")
        print(reply.fetchall())
        self.connection.commit()
    
    def client_exists(self, client_id: int) -> Boolean:
       
        reply = self.cursor.execute("SELECT username FROM clients WHERE client_id = ?", (client_id,))
        self.connection.commit()
        
        if reply.fetchone() is None:
            return False
        else:
            return True
        
    def get_clients_list(self) -> List:
        clients_list = []
        
        query = f"""
        SELECT username FROM clients        
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.connection.commit()
        
        for row in records:
            clients_list.append(row[0])
        
        return clients_list
    
     
    def get_procedures_db(self) -> List:
        procedures = []
        
        query = f"""
        SELECT procedure FROM procedures
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.connection.commit()
        
        for row in records:
            procedures.append(row[0])
            
        return procedures
    
    def get_clients_data(self) -> List:
               
        query = f"""
        SELECT client_id, username, first_name, last_name, phone_number, timing FROM clients
        """
        self.cursor.execute(query)
        client_data = self.cursor.fetchall()
        self.connection.commit()
                
        return client_data
    
    def update_procedures(self):
        db_row = []    
        
        user_data_path = Path('user_data/')
        procedures_df = pd.read_excel(user_data_path / 'procedures.xlsx').fillna("0")
        
        # очистка таблицы
        query = f"""
            DELETE FROM procedures
            """    
        self.cursor.execute(query, )
        self.connection.commit()  
        
        # сброс автоинкремента индекса таблицы
        query = f"""
            UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="procedures"
            """  
        self.cursor.execute(query, )
        self.connection.commit()  
        
        # print(procedures_df)
        for i in range(0, len(procedures_df)):
            for val in procedures_df.iloc[i]:
                db_row.append(str(val))
            query = f"""
            INSERT INTO procedures (procedure, duration, price, mon_sched, tue_sched, wed_sched, thu_sched, fri_sched, sat_sched, sun_sched) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """          
            self.cursor.execute(query, (db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5], db_row[6], db_row[7],db_row[8], db_row[9]))
            self.connection.commit()  
            db_row = []
    
    # NOT USED
    def procedure_id_from_name(self, procedure: str) -> int:
        """
        Returns the id of procedure (int) according to the provided name (string)
        """
        query = f"""
        SELECT id FROM procedures WHERE procedure=?
        """
        self.cursor.execute(query, (procedure,))
        procedure_id = self.cursor.fetchall()       
        self.connection.commit()        
                    
        return procedure_id[0][0]       
    
    # NOT USED
    def procedure_name_from_id(self, proc_id: int) -> str:
        """
        Returns the name of procedure (string) according to the provided id (int)
        """
        query = f"""
        SELECT procedure FROM procedures WHERE id=?
        """
        self.cursor.execute(query, (proc_id,))
        procedure_name = self.cursor.fetchall()       
        self.connection.commit()        
                    
        return procedure_name[0][0]        
            
    def get_procedures_data(self) -> List[Dict]:
        """
        Returns list of dicts that contain copy of procedures table in database
        
        List [Dict {id, procedure, duration, price, mon_sched, tue_sched, wed_sched, thu_sched, fri_sched, sat_sched, sun_sched}]
        """
        
        query = f"""
        SELECT id, procedure, duration, price, mon_sched, tue_sched, wed_sched, thu_sched, fri_sched, sat_sched, sun_sched FROM procedures
        """
        self.cursor.execute(query)
        procedures = self.cursor.fetchall()
        self.connection.commit()
        proc = {}   # словарь данных процедуры
        procedures_data = []    # список словарей с данными процедур
        
        for procedure in procedures:
            (proc['id'], proc['procedure'], proc['duration'], proc['price'], proc['mon_sched'], proc['tue_sched'], proc['wed_sched'], proc['thu_sched'], proc['fri_sched'], proc['sat_sched'], proc['sun_sched']) = procedure
            procedures_data.append(copy.deepcopy(proc))
                
        return procedures_data    
        
    def backup_db_file(self, db_file_name: str, description: str = ''):
        backup_file_name = f'{db_file_name.split(".")[0]}_{description}_backup_{dt.now().strftime("%y-%m-%d_%H-%M-%S")}.sqlite'
        shutil.copy(db_file_name, f'backups/{backup_file_name}')
        pass
            
    def clear_old_db_backups(self, days_old_to_delete: int, dirname: str):
        dirfiles = os.listdir(dirname)
        age = timedelta(days=days_old_to_delete)       
        for db_file in dirfiles:
            backup_date = db_file.split('_')[-2]
            date = dt.strptime(backup_date, '%y-%m-%d') 
            if date < dt.now() - age:
                print(f'file to remove - {dirname}/{db_file}')
                os.remove(f'{dirname}/{db_file}')
    
    def get_procedure_timetable(self, procedure_id: int):
        query = f"""
        SELECT mon_sched, tue_sched, wed_sched, thu_sched, fri_sched, sat_sched, sun_sched 
        FROM procedures WHERE id=?
        """
        
        try:    
            self.cursor.execute(query, (procedure_id, ))
            procedure_timetable_list = list(self.cursor.fetchall()[0])
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
        week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']        
        procedure_timetable = dict(zip(week_days, procedure_timetable_list))
        return procedure_timetable
        
    def get_occupied_periods(self, days_in_the_future: int = 30) -> list:
        query = f"""
        SELECT procedure_id, start_time, finish_time 
        FROM visits WHERE start_time BETWEEN datetime('now') AND datetime('now', ?)
        """ 
        try:    
            self.cursor.execute(query, (f'+{days_in_the_future} days', ))
            result = self.cursor.fetchall()
            self.connection.commit()
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
        occupied_periods = []
        
        for period in result:
            occupied_periods.append(p.closed(dt.strptime(period[1], '%Y-%m-%d %H:%M'), 
                                             dt.strptime(period[2], '%Y-%m-%d %H:%M')))
        
        return occupied_periods
    
    def del_client_v(self):
        query = f"""
        DELETE FROM clients 
        WHERE client_id = 631617378 OR client_id = 234637822
        """
        try:    
            self.cursor.execute(query)
            self.cursor.fetchall()
            self.connection.commit()
            
            return 'Удаление успешно'
        
        except sqlite3.Error as error:
            print('SQLite error: ', error)
            return error
        
        
db = DB_handler()