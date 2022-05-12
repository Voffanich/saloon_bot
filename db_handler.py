import sqlite3

class DB_handler():
    
    def __init__(self, dbname='saloon.sqlite'):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()
        
    def setup(self):
        query = """CREATE TABLE IF NOT EXISTS clients (
            user_name TEXT PRIMARY KEY,
            user_id INT,
            name TEXT,
            last_name TEXT,
            phone_number TEXT,
            visits_counter INT);
            """
        self.cursor.execute(query)
        self.connection.commit()
        
        query = """CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            date TEXT,
            time TEXT,
            procedure TEXT);
            """
        self.cursor.execute(query)
        self.connection.commit()
    
    def add_client(self, user_name: str, name: str = '', last_name: str = '', phone_number: str = ''):
        visits_counter = 0
        user_id = 0
        # определение максимального айдишника и назначение следующего айдишника
        query = "SELECT MAX(user_id) FROM clients"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()
        print(max_id[0])
        self.connection.commit()
        
        if type(max_id[0]) == int:
            user_id = max_id[0] + 1
        else:
            user_id = 1
        
        print(user_id)
        
        query = f"""
        INSERT INTO clients (user_name, user_id, name, last_name, phone_number, visits_counter)
        VALUES ('{user_name}', {user_id}, '{name}', '{last_name}', '{phone_number}', {visits_counter});        
        """
        self.cursor.execute(query)
        self.connection.commit()
        
    
    def add_visit(self, user_name: str, date: str, time: str, procedure: str):
        query = f"""
        
        """
        self.cursor.execute(query)
        self.connection.commit