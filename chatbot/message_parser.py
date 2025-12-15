from chatbot.patterns import *
from models.category import Category
from datetime import datetime


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

        # Check for conflicting keywords first
        has_conflict, conflicting_actions = has_conflicting_keywords(message)
        if has_conflict:
            result['intent'] = 'ambiguous'
            result['conflicting_actions'] = conflicting_actions
            return result

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

        # Update intent (e.g. "update 250 in food on december 1")
        if is_update_request(message):
            amount = extract_amount(message)
            category_info = self.match_category(message)
            date = extract_date(message)

            result['intent'] = 'update'
            result['amount'] = amount
            if category_info:
                result['category_id'] = category_info['category_id']
                result['category_name'] = category_info['category_name']
            if date:
                result['date'] = date
            return result

        # Extract transaction details for recording
        amount = extract_amount(message)
        action = extract_action(message)

        # Check if user has action keyword but no amount
        if action and not amount:
            result['intent'] = 'missing_amount'
            result['action'] = action
            return result

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