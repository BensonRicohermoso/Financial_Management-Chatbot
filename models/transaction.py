from database.db_manager import DatabaseManager
from datetime import datetime

class Transaction:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_transaction(self, transaction_type, amount, category_id, description='', date=None):
        if date is None:
            date = datetime.now()
        
        query = '''
            INSERT INTO transactions (transaction_type, amount, category_id, description, date)
            VALUES (?, ?, ?, ?, ?)
        '''
        transaction_id = self.db.execute_query(
            query, 
            (transaction_type, amount, category_id, description, date)
        )
        return transaction_id
    
    def get_transactions(self, start_date=None, end_date=None, limit=None):
        query = '''
            SELECT t.*, c.category_name, c.category_type 
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.category_id
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        if limit:
            query += ' LIMIT ?'
            params.append(limit)
        
        return self.db.fetch_all(query, tuple(params))
    
    def get_last_transaction(self):
        query = '''
            SELECT t.*, c.category_name 
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.category_id
            ORDER BY date DESC LIMIT 1
        '''
        return self.db.fetch_one(query)
    
    def delete_transaction(self, transaction_id):
        query = 'DELETE FROM transactions WHERE transaction_id = ?'
        self.db.execute_query(query, (transaction_id,))
        return True
    
    def update_transaction(self, transaction_id, **kwargs):
        allowed_fields = ['amount', 'category_id', 'description', 'date']
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f'{key} = ?')
                params.append(value)
        
        if not updates:
            return False
        
        params.append(transaction_id)
        query = f'UPDATE transactions SET {", ".join(updates)} WHERE transaction_id = ?'
        self.db.execute_query(query, tuple(params))
        return True