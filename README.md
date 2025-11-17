# Simple Bank System (Flask) — OOP + Unit Tests

This project implements a simple banking system demonstrating Object-Oriented Programming and unit testing.

Features:
- Account model (Account, SavingsAccount, CurrentAccount)
- Deposit, withdrawal, transfer
- Savings account interest calculation
- User registration & login (JSON-based simple persistence)
- Transaction history
- Unit tests (tests/test_accounts.py) verifying:
  1. Withdrawal fails if balance is insufficient.
  2. Transfer correctly updates both accounts.
  3. Interest is applied only to Savings accounts.

Run (development):
1. Create virtual env: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install: `pip install -r requirements.txt`
4. Initialize sample DB (optional): `python init_db.py`
5. Run: `python app.py`
6. Tests: `python -m unittest discover -v`

Files:
- app.py: Flask app with register/login/dashboard and transaction pages.
- models.py: OOP model classes for accounts & transactions.
- user_db.py: Simple JSON-based user and account persistence.
- templates/: HTML templates for pages.
- static/: CSS.
- tests/: Unit tests.

This is a simple educational project; do not use as-is in production.
