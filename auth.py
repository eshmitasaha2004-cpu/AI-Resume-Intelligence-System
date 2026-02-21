import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def create_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    print("ALL USERS BEFORE INSERT:", c.fetchall())
    print("USER INSERTED:", email)

    # Check if user already exists
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone():
        conn.close()
        return False

    # Insert new user
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    conn.commit()
    conn.close()
    return True


def login_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()

    conn.close()

    return user is not None