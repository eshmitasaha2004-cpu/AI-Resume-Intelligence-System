import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

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
    conn.close()


def insert_history(email, score, date):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO history VALUES (?, ?, ?)",
        (email, score, date)
    )

    conn.commit()
    conn.close()


def get_user_history(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT score, date FROM history WHERE email=?",
        (email,)
    )

    data = c.fetchall()
    conn.close()
    return data


def get_leaderboard():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT email, score FROM history ORDER BY score DESC LIMIT 5"
    )

    data = c.fetchall()
    conn.close()
    return data