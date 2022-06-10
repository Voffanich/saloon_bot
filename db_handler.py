import copy
import sqlite3
from typing import Dict, List
from xmlrpc.client import Boolean
import pandas as pd


class DB_handler():
    
    def __init__(self, dbname='saloon.sqlite'):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.flag = ''
        
    def setup(self):
        query = """CREATE TABLE IF NOT EXISTS clients (
            client_id INT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            phone_number TEXT,
            visits_counter INT,
            timing TEXT,
            last_visit TEXT,
            active TEXT,
            discount INT);
            """
        self.cursor.execute(query)
        self.connection.commit()
        
        query = """CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            date TEXT,
            start_time TEXT,
            finish_time TEXT,
            procedure TEXT,
            price INT,
            status TEXT);
            """
        self.cursor.execute(query)
        self.connection.commit()
        
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
        self.cursor.execute(query)
        self.connection.commit()
        
    def add_client(self, client_id: str, username: str, first_name: str = '', last_name: str = '', phone_number: str = '', timing: str = '2:30', last_visit: str = '', active: str = 'true', discount: int = 0):
        visits_counter = 0
        timing = '2:30'
        
        query = f"""
        INSERT INTO clients (client_id, username, first_name, last_name, phone_number, visits_counter, timing, last_visit, active, discount)
        VALUES ('{client_id}', '{username}', '{first_name}', '{last_name}', '{phone_number}', {visits_counter}, '{timing}', '{last_visit}', '{active}', '{discount}');        
        """
        self.cursor.execute(query)
        self.connection.commit()
        
    # ПЕРЕСМОТРЕТЬ ИМЕНА СТОЛБЦОВ
    def add_visit(self, client_name: str, date: str, start_time: str, finish_time: str, procedure: str, status: str, price: int = 35):
        print(client_name, date, start_time, finish_time, procedure, status, price)
        query = f"""
        INSERT INTO visits (client_name, date, start_time, finish_time, procedure, price, status)
        VALUES (?, ?, ?, ?, ?, ?, ?) 
        """
        self.cursor.execute(query, (client_name, date, start_time, finish_time, procedure, price, status, ))
        self.connection.commit
    
    def client_exists(self, username: str) -> Boolean:
       
        reply = self.cursor.execute("SELECT username FROM clients WHERE username = ?", (username,))
        self.connection.commit
        
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
        procedures_df = pd.read_excel('user_data/procedures.xlsx').fillna("0")
        
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
    def procedure_name_from_id(self, id: int) -> str:
        """
        Returns the name of procedure (string) according to the provided id (int)
        """
        query = f"""
        SELECT procedure FROM procedures WHERE id=?
        """
        self.cursor.execute(query, (id,))
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
        
        
db = DB_handler()