import sqlite3
import pandas as pd


def init_db():
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

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


def create_user(username, password):
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def verify_user(username, password):
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password),
    )
    result = c.fetchone()
    conn.close()

    return result is not None


def insert_history(user, score, date):
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO history (user, score, date) VALUES (?, ?, ?)",
        (user, score, date),
    )

    conn.commit()
    conn.close()


def get_user_history(user):
    conn = sqlite3.connect("resume.db")
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE user=? ORDER BY date ASC",
        conn,
        params=(user,),
    )
    conn.close()
    return df


def get_all_history():
    conn = sqlite3.connect("resume.db")
    df = pd.read_sql_query(
        "SELECT user, score FROM history",
        conn,
    )
    conn.close()
    return df