from database.db_manager import DatabaseManager
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
    
    def get_advice_response(self, spending_data=None):
        """Generate personalized advice"""
        base_advice = self.get_predefined_response('advice')
        
        # Add personalized advice if spending data provided
        if spending_data:
            # Future enhancement: analyze spending patterns
            pass
        
        return base_advice