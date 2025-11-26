from datetime import datetime, timedelta
from models.transaction import Transaction

class ReportGenerator:
    def __init__(self):
        self.transaction_model = Transaction()
    
    def get_date_range(self, period):
        """Get start and end date based on period"""
        now = datetime.now()
        
        if period == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        elif period == 'yesterday':
            start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(hour=23, minute=59, second=59)
        
        elif period == 'week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        elif period == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        elif period == 'year':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        
        return start, end
    
    def generate_summary(self, period='today'):
        """Generate summary report for given period"""
        start_date, end_date = self.get_date_range(period)
        transactions = self.transaction_model.get_transactions(start_date, end_date)
        
        # Calculate totals
        total_expenses = 0
        total_savings = 0
        category_breakdown = {}
        
        for trans in transactions:
            amount = trans['amount']
            category = trans['category_name'] or 'Uncategorized'
            
            if trans['transaction_type'] == 'expense':
                total_expenses += amount
                category_breakdown[category] = category_breakdown.get(category, 0) + amount
            else:
                total_savings += amount
        
        # Format response
        period_names = {
            'today': 'Today',
            'yesterday': 'Yesterday',
            'week': 'This Week',
            'month': 'This Month',
            'year': 'This Year'
        }
        
        response = f"📊 {period_names.get(period, 'Summary')} ({start_date.strftime('%b %d')} - {end_date.strftime('%b %d')})\n\n"
        response += f"💸 Total Expenses: {total_expenses:.2f} pesos\n"
        response += f"💰 Total Savings: {total_savings:.2f} pesos\n"
        response += f"📈 Net: {(total_savings - total_expenses):.2f} pesos\n"
        
        if category_breakdown:
            response += "\n📂 By Category:\n"
            for category, amount in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                response += f"  • {category}: {amount:.2f} pesos ({percentage:.1f}%)\n"
        
        return response, {
            'total_expenses': total_expenses,
            'total_savings': total_savings,
            'category_breakdown': category_breakdown,
            'transactions': transactions
        }
    
    def get_recent_transactions(self, limit=10):
        """Get recent transactions"""
        transactions = self.transaction_model.get_transactions(limit=limit)
        
        if not transactions:
            return "No transactions recorded yet."
        
        response = f"📝 Recent Transactions (Last {len(transactions)}):\n\n"
        
        for trans in transactions:
            date_str = datetime.fromisoformat(trans['date']).strftime('%b %d, %I:%M %p')
            category = trans['category_name'] or 'Uncategorized'
            symbol = "💸" if trans['transaction_type'] == 'expense' else "💰"
            
            response += f"{symbol} {trans['amount']:.2f} - {category} ({date_str})\n"
        
        return response