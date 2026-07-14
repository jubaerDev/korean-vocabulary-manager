import sqlite3
from datetime import datetime

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def add_missing_word(korean, root="", sentence="", chapter=""):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO missing_words
        (
            korean,
            root,
            sentence,
            chapter,
            status,
            created_at
        )

        VALUES
        (
            ?, ?, ?, ?, ?, ?
        )
    """,
    (
        korean,
        root,
        sentence,
        chapter,
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()