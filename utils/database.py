import sqlite3

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dictionary(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        korean TEXT UNIQUE,

        root TEXT,

        bangla TEXT,

        english TEXT,

        pos TEXT,

        topik TEXT,

        chapter TEXT,

        frequency INTEGER DEFAULT 0,

        source TEXT,

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()