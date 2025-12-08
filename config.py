import os

class Config:
    # Database configuration - use SQLite for simplicity
    # For Railway/production: set DATABASE_URL environment variable for PostgreSQL
    DATABASE_URL = None  # Disable PostgreSQL for now
    DATABASE_PATH = os.environ.get('DATABASE_PATH', '/tmp/financial_chatbot.db' if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('VERCEL') else 'financial_chatbot.db')
    
    # Use PostgreSQL only if explicitly enabled
    USE_POSTGRES = False
    
    # Flask
    SECRET_KEY = 'your-secret-key-change-in-production'
    DEBUG = True
    
    # Default categories with keywords
    DEFAULT_CATEGORIES = [
        ('Food', 'expense', 'lunch,dinner,breakfast,meal,food,restaurant,ate,eat,groceries,snack,coffee'),
        ('Transportation', 'expense', 'taxi,jeep,bus,fare,gas,commute,grab,uber,transport,travel'),
        ('Bills', 'expense', 'electricity,water,intern  et,rent,bill,utilities'),
        ('Entertainment', 'expense', 'movie,cinema,concert,game,entertainment,fun,party'),
        ('Shopping', 'expense', 'shopping,clothes,shoes,mall,bought,purchase'),
        ('Health', 'expense', 'medicine,doctor,hospital,health,medical,pharmacy'),
        ('Education', 'expense', 'school,books,tuition,education,course,training'),
        ('Miscellaneous', 'expense', 'other,misc,miscellaneous,various'),
        ('Salary', 'savings', 'salary,wage,paycheck,savings,pay'),
        ('Savings', 'savings', 'save,saved,saving,savings,deposit'),
        ('Gift', 'savings', 'gift,received,given,bonus'),
    ]
    
    # Chatbot responses
    DEFAULT_RESPONSES = [
        ('how can i save|saving tips|save money', 
         'Here are some saving tips:\n• Track all expenses daily\n• Set a monthly budget\n• Cook at home more often\n• Avoid impulse purchases\n• Use the 50-30-20 rule (50% needs, 30% wants, 20% savings)', 
         'advice'),
        ('hello|hi|hey|good morning|good afternoon', 
         'Hello! I\'m your Financial Assistant. You can:\n• Record expenses: "I spent 50 on lunch"\n• Check spending: "How much did I spend today?"\n• View reports: "Show my monthly report"', 
         'greeting'),
        ('help|what can you do|commands', 
         'I can help you:\n• Record transactions: "I spent/saved [amount] on [category]"\n• View summaries: "Show today/week/month summary"\n• Delete: "Delete last transaction"\n• Get advice: "How can I save money?"', 
         'help'),
    ]