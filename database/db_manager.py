import sqlite3
from datetime import datetime
from config import Config

class DatabaseManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                category_type TEXT NOT NULL,
                keywords TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                description TEXT,
                date DATETIME NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatbot_responses (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                keywords TEXT NOT NULL,
                response_text TEXT NOT NULL,
                response_type TEXT
            )
        ''')
        
        # Insert default categories if empty
        cursor.execute('SELECT COUNT(*) FROM categories')
        if cursor.fetchone()[0] == 0:
            for cat_name, cat_type, keywords in Config.DEFAULT_CATEGORIES:
                cursor.execute(
                    'INSERT INTO categories (category_name, category_type, keywords) VALUES (?, ?, ?)',
                    (cat_name, cat_type, keywords)
                )
        
        # Insert default responses if empty
        cursor.execute('SELECT COUNT(*) FROM chatbot_responses')
        if cursor.fetchone()[0] == 0:
            for keywords, response, resp_type in Config.DEFAULT_RESPONSES:
                cursor.execute(
                    'INSERT INTO chatbot_responses (keywords, response_text, response_type) VALUES (?, ?, ?)',
                    (keywords, response, resp_type)
                )
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid
    
    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result