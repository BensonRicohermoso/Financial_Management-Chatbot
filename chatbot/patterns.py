import re

# Regex patterns
AMOUNT_PATTERN = r'(\d+(?:\.\d{1,2})?)\s*(?:pesos?|php|₱)?'

# Action keywords
EXPENSE_KEYWORDS = [
    'spent', 'spend', 'paid', 'pay', 'bought', 'buy', 'purchase', 
    'cost', 'expense', 'used', 'consumed'
]

SAVINGS_KEYWORDS = [
    'earned', 'earn', 'saved', 'save', 'received', 'receive', 
    'savings', 'salary', 'got', 'deposited'
]

# Query keywords
QUERY_KEYWORDS = [
    'how much', 'total', 'summary', 'show', 'display', 
    'list', 'report', 'view'
]

# Time period keywords
TIME_PERIODS = {
    'today': 'today',
    'yesterday': 'yesterday',
    'this week': 'week',
    'week': 'week',
    'this month': 'month',
    'month': 'month',
    'monthly': 'month',
    'this year': 'year',
    'year': 'year',
}

# CRUD keywords
DELETE_KEYWORDS = ['delete', 'remove', 'cancel']
UPDATE_KEYWORDS = ['update', 'change', 'edit', 'modify']

# Greeting keywords
GREETING_KEYWORDS = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']

# Help keywords
HELP_KEYWORDS = ['help', 'what can you do', 'commands', 'how to use']

def extract_amount(message):
    """Extract monetary amount from message"""
    match = re.search(AMOUNT_PATTERN, message, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def extract_action(message):
    """Determine if expense or savings"""
    message_lower = message.lower()
    
    for keyword in EXPENSE_KEYWORDS:
        if keyword in message_lower:
            return 'expense'
    
    for keyword in SAVINGS_KEYWORDS:
        if keyword in message_lower:
            return 'savings'
    
    return None

def extract_time_period(message):
    """Extract time period from message"""
    message_lower = message.lower()
    
    for phrase, period in TIME_PERIODS.items():
        if phrase in message_lower:
            return period
    
    return None

def is_query(message):
    """Check if message is a query"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in QUERY_KEYWORDS)

def is_delete_request(message):
    """Check if message is delete request"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in DELETE_KEYWORDS)

def is_greeting(message):
    """Check if message is greeting"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in GREETING_KEYWORDS)

def is_help_request(message):
    """Check if message is help request"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in HELP_KEYWORDS)


def is_update_request(message):
    """Check if message is an update request"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in UPDATE_KEYWORDS)


def extract_date(message):
    """Extract a date from a message. Supports formats like 'on december 1' or 'december'.

    Returns a datetime.datetime or None.
    """
    import re
    from datetime import datetime

    message_lower = message.lower()

    months = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12
    }

    # Look for patterns like 'on december 1' or 'december 1' or 'december'
    pattern = re.compile(r"(?:on\s+)?(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)\s*(\d{1,2})?", re.IGNORECASE)
    m = pattern.search(message_lower)
    if m:
        month_str = m.group(1)
        day_str = m.group(2)
        month = months.get(month_str.lower())
        now = datetime.now()
        year = now.year
        try:
            day = int(day_str) if day_str else 1
        except Exception:
            day = 1

        try:
            return datetime(year, month, day)
        except Exception:
            return None

    return None
