import sqlite3

def init_db():
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            user TEXT,
            score INTEGER,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_history(user, score, date):
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?, ?, ?)", (user, score, date))
    conn.commit()
    conn.close()


def get_user_history(user):
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE user=?", (user,))
    data = c.fetchall()
    conn.close()
    return data


def get_leaderboard():
    conn = sqlite3.connect("resume.db")
    c = conn.cursor()
    c.execute("""
        SELECT user, MAX(score)
        FROM history
        GROUP BY user
        ORDER BY MAX(score) DESC
    """)
    data = c.fetchall()
    conn.close()
    return data