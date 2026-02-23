import sqlite3
import pandas as pd

DB_NAME = "resume.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            score INTEGER,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_history(user, score, date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO history (user, score, date) VALUES (?, ?, ?)",
        (user, score, date)
    )

    conn.commit()
    conn.close()


def get_all_history():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM history", conn)
    conn.close()
    return df