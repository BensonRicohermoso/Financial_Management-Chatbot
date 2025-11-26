import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

class ChartGenerator:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_category_pie_chart(self, category_data):
        """Generate pie chart for category breakdown"""
        if not category_data:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(category_data.keys())
        amounts = list(category_data.values())
        
        colors = plt.cm.Set3(range(len(categories)))
        
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Spending by Category', fontsize=16, fontweight='bold')
        
        # Convert to base64
        img_data = self._fig_to_base64(fig)
        plt.close(fig)
        
        return img_data
    
    def generate_spending_trend(self, transactions):
        """Generate line chart for spending trends"""
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
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(dates, amounts, marker='o', linewidth=2, markersize=6, color='#e74c3c')
        ax.fill_between(dates, amounts, alpha=0.3, color='#e74c3c')
        
        ax.set_title('Daily Spending Trend', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount (Pesos)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        img_data = self._fig_to_base64(fig)
        plt.close(fig)
        
        return img_data
    
    def generate_savings_vs_expense_chart(self, data):
        """Generate bar chart comparing savings vs expenses"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        categories = ['Savings', 'Expenses', 'Net']
        amounts = [
            data.get('total_savings', 0),
            data.get('total_expenses', 0),
            data.get('total_savings', 0) - data.get('total_expenses', 0)
        ]
        colors = ['#2ecc71', '#e74c3c', '#3498db']
        
        bars = ax.bar(categories, amounts, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'₱{height:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Savings vs Expenses', fontsize=16, fontweight='bold')
        ax.set_ylabel('Amount (Pesos)', fontsize=12)
        ax.grid(True, axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        img_data = self._fig_to_base64(fig)
        plt.close(fig)
        
        return img_data
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img_base64