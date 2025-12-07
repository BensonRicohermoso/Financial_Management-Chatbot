from datetime import datetime

class ChartGenerator:
    def __init__(self):
        pass
    
    def generate_category_pie_chart(self, category_data):
        """Generate chart data for category breakdown (JSON for frontend)"""
        if not category_data:
            return None
        
        return {
            'type': 'pie',
            'labels': list(category_data.keys()),
            'data': list(category_data.values())
        }
    
    def generate_spending_trend(self, transactions):
        """Generate chart data for spending trends (JSON for frontend)"""
        if not transactions:
            return None
        
        # Group by date
        daily_spending = {}
        
        for trans in transactions:
            if trans['transaction_type'] == 'expense':
                date = datetime.fromisoformat(trans['date']).date()
                daily_spending[date] = daily_spending.get(date, 0) + trans['amount']
        
        if not daily_spending:
            return None
        
        # Sort by date
        dates = sorted(daily_spending.keys())
        amounts = [daily_spending[date] for date in dates]
        
        return {
            'type': 'line',
            'labels': [d.strftime('%Y-%m-%d') for d in dates],
            'data': amounts
        }
    
    def generate_savings_vs_expense_chart(self, data):
        """Generate chart data comparing savings vs expenses (JSON for frontend)"""
        return {
            'type': 'bar',
            'labels': ['Savings', 'Expenses', 'Net'],
            'data': [
                data.get('total_savings', 0),
                data.get('total_expenses', 0),
                data.get('total_savings', 0) - data.get('total_expenses', 0)
            ]
        }