from user_db import create_user
if __name__ == "__main__":
    try:
        create_user("alice", "password123", "Alice Example")
        create_user("bob", "password123", "Bob Example")
        print("Sample users alice, bob created (password: password123).")
    except Exception as e:
        print("Error:", e)
