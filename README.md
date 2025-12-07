# Financial Management Chatbot (FinBot AI)

A modern, mobile-responsive Flask-based chatbot for tracking personal finances. Record transactions through natural language, view interactive analytics with Chart.js visualizations, and manage your budget effortlessly.

## ✨ Features

- 💬 **Natural Language Processing** - Record transactions conversationally (e.g., "spent 150 on groceries")
- 📊 **Interactive Analytics** - Beautiful Chart.js visualizations (pie charts, line graphs, bar charts)
- 📱 **Fully Responsive** - Optimized for mobile, tablet, and desktop
- 🔄 **CRUD Operations** - Create, read, update, and delete transactions
- 📈 **Time-based Reports** - View summaries for today, week, month, or year
- 🎨 **Modern UI** - Clean gradient design with smooth animations
- ☁️ **Cloud Ready** - Deployable to Vercel with minimal configuration

## 🎯 Supported Commands

### Record Transactions

- `spent 200 on groceries`
- `paid 50 for lunch`
- `saved 1000`
- `earned 5000 salary`

### Query Summaries

- `show today summary`
- `how much spent this week`
- `display monthly report`

### Update Transactions

- `update 250 in food on december 1`
- `change 100 in transport on december 5`

### Delete & Help

- `delete last transaction`
- `help` - View all commands
- `hi` or `hello` - Greeting

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**

```powershell
git clone https://github.com/BensonRicohermoso/Financial_Management-Chatbot.git
cd Financial_Management-Chatbot
```

2. **Create and activate virtual environment:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
source venv/bin/activate      # Linux/Mac
```

3. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

4. **Run the application:**

```powershell
python app.py
```

5. **Open in browser:**

```
http://127.0.0.1:5000/
```

## 📁 Project Structure

```
financial_chatbot/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel deployment config
├── runtime.txt                 # Python runtime version
├── chatbot/
│   ├── message_parser.py       # NLP message parsing
│   ├── patterns.py             # Regex patterns & keyword matching
│   └── response_generator.py   # Response generation logic
├── database/
│   └── db_manager.py           # SQLite database manager
├── models/
│   ├── transaction.py          # Transaction CRUD operations
│   └── category.py             # Category management
├── analytics/
│   ├── report_generator.py     # Summary reports
│   └── chart_generator.py      # Chart data generation (JSON)
├── templates/
│   ├── index.html              # Chat interface
│   └── analytics.html          # Analytics dashboard
└── static/
    └── images/                 # Logos and favicons

```

## 🛠️ Technology Stack

**Backend:**

- Flask 3.0+ (Python web framework)
- SQLite (local database)
- python-dateutil (date parsing)

**Frontend:**

- HTML5/CSS3 with responsive design
- Vanilla JavaScript (ES6+)
- Chart.js 4.4+ (interactive charts)

**Deployment:**

- Vercel (serverless hosting)
- Python 3.9 runtime

## ☁️ Deploying to Vercel

This application is optimized for Vercel deployment with serverless functions.

### Quick Deploy

1. **Install Vercel CLI:**

```powershell
npm i -g vercel
```

2. **Deploy:**

```powershell
vercel
```

3. **Follow the prompts** to link/create your Vercel project

### Important Notes

⚠️ **Database Limitations on Vercel:**

- SQLite database uses `/tmp` storage (ephemeral)
- Data resets between deployments and cold starts
- **Not suitable for production without migration to persistent DB**

🔄 **For Production Use:**

- Migrate to Vercel Postgres, Supabase, PlanetScale, or Railway
- Update `database/db_manager.py` to use cloud database
- Add connection string as environment variable in Vercel

### Configuration Files

- `vercel.json` - Routes all requests to Flask app
- `runtime.txt` - Specifies Python 3.9 runtime
- `.vercelignore` - Excludes unnecessary files from deployment

## 📱 Mobile Responsiveness

The application is fully responsive with breakpoints at:

- **Desktop:** 769px+ (full layout)
- **Tablet:** 768px (optimized grid)
- **Mobile:** 480px (stacked layout)
- **Landscape mode:** Special optimizations

Features:

- Touch-friendly buttons and inputs
- Responsive charts with adaptive sizing
- Optimized font sizes and spacing
- Full-screen mobile experience

## 🔌 API Endpoints

### POST `/chat`

Process chat messages and execute commands.

**Request:**

```json
{
  "message": "spent 150 on groceries"
}
```

**Response:**

```json
{
  "response": "✓ Recorded: 150 pesos spent on Food",
  "intent": "record_transaction",
  "chart": null
}
```

### GET `/api/summary/<period>`

Get financial summary for time period.

**Parameters:** `period` - `today`, `week`, `month`, `year`

**Response:**

```json
{
  "summary": "Today's Summary...",
  "data": {
    "total_expenses": 500.00,
    "total_savings": 1000.00,
    "net": 500.00,
    "category_breakdown": {
      "Food": 300,
      "Transport": 200
    }
  },
  "charts": {
    "pie": { "type": "pie", "labels": [...], "data": [...] },
    "trend": { "type": "line", "labels": [...], "data": [...] },
    "comparison": { "type": "bar", "labels": [...], "data": [...] }
  }
}
```

### GET `/api/transactions/recent`

Get recent transactions (last 20).

## 🎨 Customization

### Adding Categories

Edit `config.py` to add new expense/savings categories:

```python
DEFAULT_CATEGORIES = [
    ('Category Name', 'expense', 'keyword1,keyword2,keyword3'),
    # Add more...
]
```

### Chart Colors

Modify chart colors in `templates/analytics.html`:

```javascript
backgroundColor: [
  "rgba(231, 76, 60, 0.7)", // Red
  "rgba(52, 152, 219, 0.7)", // Blue
  // Add more colors...
];
```

## 🧪 Testing

### Test Chat Endpoint

```powershell
curl -H "Content-Type: application/json" -X POST -d "{\"message\":\"spent 100 on food\"}" http://127.0.0.1:5000/chat
```

### Test Summary API

```powershell
curl http://127.0.0.1:5000/api/summary/today
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Write clear commit messages
- Add comments for complex logic
- Test locally before pushing
- Keep PRs focused and small
- Update README for new features

## 🐛 Troubleshooting

### Database Issues

**Problem:** Transactions not persisting on Vercel
**Solution:** Migrate to persistent database (Vercel Postgres, Supabase, etc.)

### Chart Not Displaying

**Problem:** Charts show as corrupted/missing
**Solution:** Ensure Chart.js CDN is loaded and check browser console for errors

### Vercel Build Fails

**Problem:** `pip install` errors
**Solution:** Check `requirements.txt` has correct versions and `runtime.txt` specifies Python 3.9

### Import Errors Locally

**Problem:** Module not found errors
**Solution:** Activate virtual environment and reinstall: `pip install -r requirements.txt`

## 📄 License

This project is provided as-is for educational and personal use.

For commercial use or distribution, please add an appropriate open-source license (MIT, Apache 2.0, etc.).

## 👨‍💻 Author

**Benson Ricohermoso**

- GitHub: [@BensonRicohermoso](https://github.com/BensonRicohermoso)
- Repository: [Financial_Management-Chatbot](https://github.com/BensonRicohermoso/Financial_Management-Chatbot)

## 🙏 Acknowledgments

- **Flask** - Python web framework
- **Chart.js** - Beautiful JavaScript charts
- **Vercel** - Serverless deployment platform

---

**Built with ❤️ for smarter financial management**

_Last updated: December 8, 2025_
