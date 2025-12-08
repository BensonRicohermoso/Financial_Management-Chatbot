import sqlite3
from datetime import datetime
from config import Config

# Try to import psycopg2, but don't fail if not available
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

class DatabaseManager:
    def __init__(self, db_path=None):
        self.use_postgres = Config.USE_POSTGRES and HAS_POSTGRES
        if self.use_postgres:
            self.db_url = Config.DATABASE_URL
        else:
            self.db_path = db_path or Config.DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        if self.use_postgres:
            # Add SSL mode for Railway/cloud PostgreSQL
            conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor, sslmode='require')
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            # PostgreSQL table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    category_id SERIAL PRIMARY KEY,
                    category_name TEXT UNIQUE NOT NULL,
                    category_type TEXT NOT NULL,
                    keywords TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id SERIAL PRIMARY KEY,
                    transaction_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category_id INTEGER,
                    description TEXT,
                    date TIMESTAMP NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chatbot_responses (
                    response_id SERIAL PRIMARY KEY,
                    keywords TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    response_type TEXT
                )
            ''')
        else:
            # SQLite table creation
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
        count = cursor.fetchone()
        if (count[0] if self.use_postgres else count[0]) == 0:
            for cat_name, cat_type, keywords in Config.DEFAULT_CATEGORIES:
                cursor.execute(
                    'INSERT INTO categories (category_name, category_type, keywords) VALUES (%s, %s, %s)' if self.use_postgres
                    else 'INSERT INTO categories (category_name, category_type, keywords) VALUES (?, ?, ?)',
                    (cat_name, cat_type, keywords)
                )
        
        # Insert default responses if empty
        cursor.execute('SELECT COUNT(*) FROM chatbot_responses')
        count = cursor.fetchone()
        if (count[0] if self.use_postgres else count[0]) == 0:
            for keywords, response, resp_type in Config.DEFAULT_RESPONSES:
                cursor.execute(
                    'INSERT INTO chatbot_responses (keywords, response_text, response_type) VALUES (%s, %s, %s)' if self.use_postgres
                    else 'INSERT INTO chatbot_responses (keywords, response_text, response_type) VALUES (?, ?, ?)',
                    (keywords, response, resp_type)
                )
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def execute_query(self, query, params=()):
        # Convert ? to %s for PostgreSQL
        if self.use_postgres:
            query = query.replace('?', '%s')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        lastrowid = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
        cursor.close()
        conn.close()
        return lastrowid
    
    def fetch_all(self, query, params=()):
        # Convert ? to %s for PostgreSQL
        if self.use_postgres:
            query = query.replace('?', '%s')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def fetch_one(self, query, params=()):
        # Convert ? to %s for PostgreSQL
        if self.use_postgres:
            query = query.replace('?', '%s')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result