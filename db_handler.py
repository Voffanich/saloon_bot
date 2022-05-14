from http import client
import sqlite3
from typing import List
from xmlrpc.client import Boolean

class DB_handler():
    
    def __init__(self, dbname='saloon.sqlite'):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.flag = ''
        
    def setup(self):
        query = """CREATE TABLE IF NOT EXISTS clients (
            client_name TEXT PRIMARY KEY,
            client_id INT,
            name TEXT,
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
    
    def add_client(self, client_name: str, name: str = '', last_name: str = '', phone_number: str = '', timing: str = '2:30', last_visit: str = '', active: str = 'true', discount: int = 0):
        visits_counter = 0
        client_id = 0
        # определение максимального айдишника и назначение следующего айдишника
        query = "SELECT MAX(client_id) FROM clients"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()
        #print(max_id[0])
        self.connection.commit()
        
        if type(max_id[0]) == int:
            client_id = max_id[0] + 1
        else:
            client_id = 1
        
        #print(client_id)
        
        query = f"""
        INSERT INTO clients (client_name, client_id, name, last_name, phone_number, visits_counter, timing, last_visit, active, discount)
        VALUES ('{client_name}', {client_id}, '{name}', '{last_name}', '{phone_number}', {visits_counter}, '{timing}', '{last_visit}', '{active}', '{discount}');        
        """
        self.cursor.execute(query)
        self.connection.commit()
        
    
    def add_visit(self, client_name: str, date: str, start_time: str, finish_time: str, procedure: str, status: str, price: int = 35):
        query = f"""
        INSERT INTO visits (id, client_name, date, start_time, finish_time, procedure, price, status)
        VALUES ('{client_name}', {date}, '{start_time}', '{finish_time}', '{procedure}', {status}, {price}'); 
        """
        self.cursor.execute(query)
        self.connection.commit
    
    def client_exists(self, client_name: str) -> Boolean:
       
        reply = self.cursor.execute("SELECT client_name FROM clients WHERE client_name = ?", (client_name,))
        self.connection.commit
        
        if reply.fetchone() is None:
            return False
        else:
            return True
        
    def clients_list(self) -> List:
        clients_list = []
        
        query = f"""
        SELECT client_name FROM clients        
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.connection.commit()
        
        for row in records:
            clients_list.append(row[0])
        
        return clients_list