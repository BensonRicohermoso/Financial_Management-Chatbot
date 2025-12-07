from flask import Flask, render_template, request, jsonify
from chatbot.message_parser import MessageParser
from chatbot.response_generator import ResponseGenerator
from models.transaction import Transaction
from analytics.report_generator import ReportGenerator
from analytics.chart_generator import ChartGenerator
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
parser = MessageParser()
response_gen = ResponseGenerator()
transaction_model = Transaction()
report_gen = ReportGenerator()
chart_gen = ChartGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})
    
    # Parse message
    parsed = parser.parse_message(user_message)
    intent = parsed['intent']
    
    response_text = ''
    chart_data = None
    
    # Handle different intents
    if intent == 'record_transaction':
        # Record transaction
        transaction_id = transaction_model.create_transaction(
            transaction_type=parsed['action'],
            amount=parsed['amount'],
            category_id=parsed['category_id'],
            description=parsed['description'],
            date=parsed['date']
        )
        
        response_text = response_gen.generate_response(
            intent,
            amount=parsed['amount'],
            category_name=parsed['category_name'] or 'Miscellaneous',
            action=parsed['action']
        )
    
    elif intent == 'query':
        period = parsed['time_period'] or 'today'
        response_text, data = report_gen.generate_summary(period)
    
    elif intent == 'delete':
        last_transaction = transaction_model.get_last_transaction()
        if last_transaction:
            transaction_model.delete_transaction(last_transaction['transaction_id'])
        response_text = response_gen.generate_response(intent, transaction=last_transaction)

    elif intent == 'update':
        # Attempt to perform update based on parsed fields
        response_text = response_gen.generate_response(
            intent,
            amount=parsed.get('amount'),
            category_id=parsed.get('category_id'),
            category_name=parsed.get('category_name'),
            date=parsed.get('date')
        )
    
    elif intent in ['greeting', 'help', 'advice']:
        response_text = response_gen.generate_response(intent)
    
    else:
        response_text = response_gen.generate_response('unknown')
    
    return jsonify({
        'response': response_text,
        'intent': intent,
        'chart': chart_data
    })

@app.route('/api/summary/<period>')
def get_summary(period):
    response_text, data = report_gen.generate_summary(period)
    
    # Generate charts
    pie_chart = None
    trend_chart = None
    comparison_chart = None
    
    if data['category_breakdown']:
        pie_chart = chart_gen.generate_category_pie_chart(data['category_breakdown'])
    
    if data['transactions']:
        trend_chart = chart_gen.generate_spending_trend(data['transactions'])
    
    comparison_chart = chart_gen.generate_savings_vs_expense_chart(data)
    
    return jsonify({
        'summary': response_text,
        'data': {
            'total_expenses': data['total_expenses'],
            'total_savings': data.get('total_savings', 0),
            'net': data.get('total_savings', 0) - data['total_expenses'],
            'category_breakdown': data['category_breakdown']
        },
        'charts': {
            'pie': pie_chart,
            'trend': trend_chart,
            'comparison': comparison_chart
        }
    })

@app.route('/api/transactions/recent')
def get_recent_transactions():
    response = report_gen.get_recent_transactions(limit=20)
    return jsonify({'response': response})

if __name__ == '__main__':
    # Disable the automatic reloader so the server runs in this process
    # and logs appear reliably in the terminal.
    app.run(debug=True, port=5000, use_reloader=False)

# For Vercel deployment - export app at module level
application = app