import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dictionary(
        korean TEXT PRIMARY KEY,
        bangla TEXT,
        english TEXT,
        pos TEXT,
        topik TEXT
    )
    """)

    conn.commit()
    conn.close()


def import_dictionary(df):

    create_table()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    added = 0
    updated = 0
    skipped = 0

    for _, row in df.iterrows():

        korean = str(row.get("Korean","")).strip()

        if korean == "":
            skipped += 1
            continue

        bangla = str(row.get("Bangla","")).strip()
        english = str(row.get("English","")).strip()
        pos = str(row.get("POS","")).strip()
        topik = str(row.get("TOPIK","")).strip()

        cur.execute(
            "SELECT korean FROM dictionary WHERE korean=?",
            (korean,)
        )

        if cur.fetchone():

            cur.execute("""
            UPDATE dictionary
            SET
                bangla=?,
                english=?,
                pos=?,
                topik=?
            WHERE korean=?
            """,
            (bangla, english, pos, topik, korean))

            updated += 1

        else:

            cur.execute("""
            INSERT INTO dictionary
            VALUES(?,?,?,?,?)
            """,
            (korean, bangla, english, pos, topik))

            added += 1

    conn.commit()
    conn.close()

    return added, updated, skipped
