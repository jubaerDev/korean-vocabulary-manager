import sqlite3

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cur = conn.cursor()

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

    # Upgrade old database
    cur.execute("PRAGMA table_info(dictionary)")
    existing = [row[1] for row in cur.fetchall()]

    new_columns = {
        "example_kr": "TEXT",
        "example_bn": "TEXT",
        "notes": "TEXT",
        "favorite": "INTEGER DEFAULT 0",
        "search_count": "INTEGER DEFAULT 0",
        "updated_at": "TEXT"
    }

    for col, dtype in new_columns.items():
        if col not in existing:
            cur.execute(f"ALTER TABLE dictionary ADD COLUMN {col} {dtype}")

    conn.commit()
    conn.close()


create_database()