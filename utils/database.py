import sqlite3

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cur = conn.cursor()

    # -------- Dictionary Table --------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dictionary (

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

        example_kr TEXT,

        example_bn TEXT,

        notes TEXT,

        favorite INTEGER DEFAULT 0,

        search_count INTEGER DEFAULT 0,

        created_at TEXT,

        updated_at TEXT

    )
    """)

    # -------- Missing Words Table --------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS missing_words (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        korean TEXT UNIQUE,

        root TEXT,

        sentence TEXT,

        chapter TEXT,

        status TEXT DEFAULT 'Pending',

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()

create_database()