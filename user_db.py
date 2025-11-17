import json
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from models import SavingsAccount, CurrentAccount
DB_FILE = Path(__file__).parent / "data" / "users.json"

def _ensure_db():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": {}}, f)

def load_db():
    _ensure_db()
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    _ensure_db()
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def create_user(username, password, full_name=""):
    data = load_db()
    if username in data["users"]:
        raise ValueError("User exists")
    hashed = generate_password_hash(password)
    # create a basic savings and current account per user
    savings = SavingsAccount(owner=username, balance=0.0).to_dict()
    current = CurrentAccount(owner=username, balance=0.0).to_dict()
    data["users"][username] = {
        "password": hashed,
        "full_name": full_name,
        "accounts": {
            "savings": savings,
            "current": current
        }
    }
    save_db(data)
    return data["users"][username]

def verify_user(username, password):
    data = load_db()
    if username not in data["users"]:
        return False
    return check_password_hash(data["users"][username]['password'], password)

def get_user(username):
    data = load_db()
    return data["users"].get(username)

def update_user(username, userobj):
    data = load_db()
    data["users"][username] = userobj
    save_db(data)
