import os
import sqlite3

DB_PATH = os.path.join(os.getcwd(), "users.db")

# Ensure DB file exists
if not os.path.exists(DB_PATH):
    open(DB_PATH, "w").close()

# Create global connection
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()


def init_db():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            email TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS history(
            email TEXT,
            score REAL,
            date TEXT
        )
    """)

    conn.commit()


def insert_history(email, score, date):
    c.execute(
        "INSERT INTO history (email, score, date) VALUES (?, ?, ?)",
        (email, score, date)
    )
    conn.commit()


def get_user_history(email):
    c.execute(
        "SELECT score, date FROM history WHERE email=?",
        (email,)
    )
    data = c.fetchall()
    return data


def get_leaderboard():
    c.execute(
        "SELECT email, MAX(score) as best_score FROM history GROUP BY email ORDER BY best_score DESC LIMIT 5"
    )
    data = c.fetchall()
    return data
