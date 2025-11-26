# Financial Management Chatbot

This is a small Flask-based financial chatbot that records transactions, shows analytics, and generates charts.

Quick start (Windows / PowerShell):

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

Notes:
- Keep secrets and local DB files out of git (they are listed in `.gitignore`).
- If you want to split frontend/backend into separate repos later, consider extracting `templates/` and `static/`.
