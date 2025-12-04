from database.db_manager import DatabaseManager
from models.transaction import Transaction
from datetime import datetime, timedelta
import re

class ResponseGenerator:
    def __init__(self):
        self.db = DatabaseManager()
    
    def generate_response(self, intent, **kwargs):
        """Generate appropriate response based on intent"""
        
        if intent == 'greeting':
            return self.get_predefined_response('greeting')
        
        elif intent == 'help':
            return self.get_predefined_response('help')
        
        elif intent == 'advice':
            return self.get_advice_response(kwargs.get('spending_data'))
        
        elif intent == 'record_transaction':
            return self.transaction_recorded_response(
                kwargs.get('amount'),
                kwargs.get('category_name'),
                kwargs.get('action')
            )

        elif intent == 'update':
            return self.update_transaction_response(
                kwargs.get('amount'),
                kwargs.get('category_id'),
                kwargs.get('category_name'),
                kwargs.get('date')
            )
        
        elif intent == 'query':
            return None  # Handle in analytics
        
        elif intent == 'delete':
            return self.delete_confirmation_response(kwargs.get('transaction'))
        
        else:
            return "I'm not sure what you mean. Try saying 'spent 50 on lunch' or 'show today summary'"
    
    def get_predefined_response(self, response_type):
        """Get predefined response from database"""
        query = 'SELECT response_text FROM chatbot_responses WHERE response_type = ? LIMIT 1'
        result = self.db.fetch_one(query, (response_type,))
        
        if result:
            return result['response_text']
        return "Hello! How can I help you today?"
    
    def transaction_recorded_response(self, amount, category_name, action):
        """Generate response for recorded transaction"""
        action_text = "spent on" if action == "expense" else "saved in"
        category_text = category_name if category_name else "Miscellaneous"
        
        return f"✓ Recorded: {amount} pesos {action_text} {category_text}"
    
    def delete_confirmation_response(self, transaction):
        """Generate response for deleted transaction"""
        if transaction:
            return f"✓ Deleted: {transaction['amount']} pesos on {transaction['category_name']}"
        return "No recent transaction to delete."

    def update_transaction_response(self, amount, category_id, category_name, date):
        """Update a matching transaction's amount (most-recent match) and return a response."""
        if amount is None:
            return "I couldn't find the new amount to update. Please say something like 'update 250 in food on december 1'"

        if not category_id:
            return "I couldn't determine the category to update. Please include a category name."

        if not date:
            return "I couldn't find a date to match. Please include a date like 'on December 1'."

        txn_model = Transaction()

        # Build start and end of day strings
        try:
            start_dt = datetime(date.year, date.month, date.day, 0, 0, 0)
            end_dt = datetime(date.year, date.month, date.day, 23, 59, 59)
        except Exception:
            return "The date you provided looks invalid. Please try a different date."

        start_str = start_dt.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Fetch transactions in that date range
        transactions = txn_model.get_transactions(start_date=start_str, end_date=end_str)

        # Find the most recent transaction matching the category
        matching = None
        for t in transactions:
            # t may have category_id as integer or None
            if t['category_id'] == category_id:
                matching = t
                break

        if not matching:
            return "No matching transaction found for that category and date."

        # Update the transaction amount
        txn_model.update_transaction(matching['transaction_id'], amount=amount)

        cat_name = category_name or 'Miscellaneous'
        return f"✓ Updated: set {cat_name} on {start_dt.strftime('%Y-%m-%d')} to {amount} pesos"
    
    def get_advice_response(self, spending_data=None):
        """Generate personalized advice"""
        base_advice = self.get_predefined_response('advice')
        
        # Add personalized advice if spending data provided
        if spending_data:
            # Future enhancement: analyze spending patterns
            pass
        
        return base_advice