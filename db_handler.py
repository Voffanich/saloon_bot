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
        self.connection.commit
        
        query = """CREATE TABLE IF NOT EXISTS visits (
            user_name TEXT PRIMARY KEY,
            date TEXT,
            time TEXT
            procedure TEXT);
            """
        self.cursor.execute(query)
        self.connection.commit
    
    def add_client(self, user_name: str, name: str = '', last_name: str = '', phone_number: str = ''):
        visits_counter = 0
        query = "SELECT MAX(user_id) FROM clients"
        self.cursor.execute(query)
        user_id = self.cursor.fetchone()
        self.connection.commit
        
        if type(user_id) == int:
            user_id += 1
        else:
            user_id = 1
        
        print(user_id)
        
        query = f"""
        INSERT INTO clients (user_name, user_id, name, last_name, phone_number, visits_counter)
        VALUES ({user_name}, {user_id}, {name}, {last_name}, {phone_number}, {visits_counter});        
        """
        self.cursor.execute(query)
        self.connection.commit
    
    def add_visit(self, client: str, date: str, time: str, procedure: str):
        query = f"""
        
        """
        self.cursor.execute(query)
        self.connection.commit