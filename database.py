import os
import sqlite3

DB_PATH = "users.db"
if not os.path.exists(DB_PATH):
    open(DB_PATH, "W").close()

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
    conn.close()


def insert_history(email, score, date):
   global conn, c

c.execute(
        "INSERT INTO history VALUES (?, ?, ?)",
        (email, score, date)
    )

conn.commit()
conn.close()


def get_user_history(email):
    global conn,
    c = conn.cursor()

    c.execute(
        "SELECT score, date FROM history WHERE email=?",
        (email,)
    )

    data = c.fetchall()
    conn.close()
    return data


def get_leaderboard():
    global conn, c
    c = conn.cursor()

    c.execute(
        "SELECT email, score FROM history ORDER BY score DESC LIMIT 5"
    )

    data = c.fetchall()
    conn.close()
    return data