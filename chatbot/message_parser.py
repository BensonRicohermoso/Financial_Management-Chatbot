from chatbot.patterns import *
from models.category import Category
from datetime import datetime, timedelta

class MessageParser:
    def __init__(self):
        self.category_model = Category()
        self.categories_dict = self.category_model.get_categories_dict()
    
    def parse_message(self, message):
        """Parse user message and extract all relevant information"""
        result = {
            'intent': None,
            'amount': None,
            'action': None,
            'category_id': None,
            'category_name': None,
            'description': message,
            'time_period': None,
            'date': datetime.now()
        }
        
        # Determine intent
        if is_greeting(message):
            result['intent'] = 'greeting'
            return result
        
        if is_help_request(message):
            result['intent'] = 'help'
            return result
        
        if is_delete_request(message):
            result['intent'] = 'delete'
            return result
        
        if is_query(message):
            result['intent'] = 'query'
            result['time_period'] = extract_time_period(message)
            return result
        
        # Extract transaction details
        amount = extract_amount(message)
        action = extract_action(message)
        
        if amount and action:
            result['intent'] = 'record_transaction'
            result['amount'] = amount
            result['action'] = action
            
            # Match category
            category_info = self.match_category(message)
            if category_info:
                result['category_id'] = category_info['category_id']
                result['category_name'] = category_info['category_name']
            
            return result
        
        # Check if it's an advice request
        if 'save' in message.lower() or 'advice' in message.lower() or 'tip' in message.lower():
            result['intent'] = 'advice'
            return result
        
        result['intent'] = 'unknown'
        return result
    
    def match_category(self, message):
        """Match message against category keywords"""
        message_lower = message.lower()
        words = message_lower.split()
        
        # Check each word against keywords
        for word in words:
            if word in self.categories_dict:
                return self.categories_dict[word]
        
        # Check multi-word phrases
        for keyword, category_info in self.categories_dict.items():
            if keyword in message_lower:
                return category_info
        
        return None

from chatbot.patterns import *
from models.category import Category
from datetime import datetime, timedelta

class MessageParser:
    def __init__(self):
        self.category_model = Category()
        self.categories_dict = self.category_model.get_categories_dict()
    
    def parse_message(self, message):
        """Parse user message and extract all relevant information"""
        result = {
            'intent': None,
            'amount': None,
            'action': None,
            'category_id': None,
            'category_name': None,
            'description': message,
            'time_period': None,
            'date': datetime.now()
        }
        
        # Determine intent
        if is_greeting(message):
            result['intent'] = 'greeting'
            return result
        
        if is_help_request(message):
            result['intent'] = 'help'
            return result
        
        if is_delete_request(message):
            result['intent'] = 'delete'
            return result
        
        if is_query(message):
            result['intent'] = 'query'
            result['time_period'] = extract_time_period(message)
            return result
        
        # Extract transaction details
        amount = extract_amount(message)
        action = extract_action(message)
        
        if amount and action:
            result['intent'] = 'record_transaction'
            result['amount'] = amount
            result['action'] = action
            
            # Match category
            category_info = self.match_category(message)
            if category_info:
                result['category_id'] = category_info['category_id']
                result['category_name'] = category_info['category_name']
            
            return result
        
        # Check if it's an advice request
        if 'save' in message.lower() or 'advice' in message.lower() or 'tip' in message.lower():
            result['intent'] = 'advice'
            return result
        
        result['intent'] = 'unknown'
        return result
    
    def match_category(self, message):
        """Match message against category keywords"""
        message_lower = message.lower()
        words = message_lower.split()
        
        # Check each word against keywords
        for word in words:
            if word in self.categories_dict:
                return self.categories_dict[word]
        
        # Check multi-word phrases
        for keyword, category_info in self.categories_dict.items():
            if keyword in message_lower:
                return category_info
        
        return None