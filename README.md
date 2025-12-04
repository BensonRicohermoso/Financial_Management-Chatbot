# Financial Management Chatbot

A compact Flask-based chatbot for tracking personal finances. It records transactions (expenses/savings), stores them in a local SQLite database, and provides simple analytics and charts.

This repository contains the backend Flask application, simple templates for a minimal UI, and modules for parsing natural-language messages to record, query, delete, and update transactions.

## Features

- Record transactions by natural language (e.g. "spent 150 on groceries").
- Query summaries (today, this week, month).
- Delete the most recent transaction.
- Update existing transactions using phrases like: `update 250 in food on december 1`.
- Simple analytics and chart generation (category breakdown, trends).

## Quick start (Windows / PowerShell)

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

4. Open the UI in your browser:

```
http://127.0.0.1:5000/
```

## Usage examples

- Record an expense: `spent 200 on groceries`
- Record savings: `saved 1000`
- Query today's summary: `show today summary` or `how much spent today`
- Delete most recent transaction: `delete last transaction` (or just `delete`)
- Update a transaction (example):

```
update 250 in food on december 1
```

The update flow attempts to find the most recent transaction on the specified date with the matching category and sets its amount to the new value.

## Project structure

- `app.py` — Flask app and API routes.
- `chatbot/` — message parsing and response generation logic.
- `database/` — `db_manager.py` manages the SQLite DB and schema.
- `models/` — data models (e.g., `transaction.py`, `category.py`).
- `analytics/` — summary and chart generation utilities.
- `templates/` and `static/` — minimal frontend UI.

## Development notes

- The app uses SQLite by default. The database file path is configured in `config.py`.
- Date parsing for updates supports month names with optional day (e.g., "December 1"). For more flexible parsing consider adding the `dateparser` package.
- When rebasing or merging, keep an eye on templates and README conflicts — they are commonly edited.

## Testing locally

- Start the app and use the chat input on the UI.
- You can also call the `/chat` endpoint with JSON (e.g., via `curl` or Postman):

```powershell
curl -H "Content-Type: application/json" -X POST -d '{"message":"update 250 in food on december 1"}' http://127.0.0.1:5000/chat
```

## Contributing

- Open issues or PRs for improvements. Prefer feature branches and small PRs.

## License

This project is provided as-is. Add a license file if you plan to publish or distribute it.

---

_Generated/updated README on Dec 5, 2025_
