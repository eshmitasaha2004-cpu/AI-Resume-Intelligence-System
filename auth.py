import sqlite3

DB_PATH = "users.db"

def create_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

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