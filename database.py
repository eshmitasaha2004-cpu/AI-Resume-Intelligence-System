import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        match_score REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_history(user, score, timestamp):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    INSERT INTO history (user_email, match_score, timestamp)
    VALUES (?, ?, ?)
    """, (user, score, timestamp))
    conn.commit()
    conn.close()

def get_user_history(user):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT match_score, timestamp FROM history WHERE user_email=?", (user,))
    data = c.fetchall()
    conn.close()
    return data

def get_leaderboard():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    SELECT user_email, MAX(match_score) as best_score
    FROM history
    GROUP BY user_email
    ORDER BY best_score DESC
    LIMIT 5
    """)
    data = c.fetchall()
    conn.close()
    return data
