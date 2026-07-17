import sqlite3
import pandas as pd

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
    # -------- Common Words Table --------

    cur.execute("""
    CREATE TABLE IF NOT EXISTS common_words (

       id INTEGER PRIMARY KEY AUTOINCREMENT,

       korean TEXT UNIQUE,

       bangla TEXT,

       source TEXT,

       created_at TEXT DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()
    conn.close()

create_database()
# ==========================================
# Common Words Functions
# ==========================================

def get_common_connection():

    return sqlite3.connect(DB_PATH)


def total_common_words():

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM common_words
        """
    )

    total = cur.fetchone()[0]

    conn.close()

    return total
# ==========================================
# Import Common Words
# ==========================================

from datetime import datetime


def import_common_word(
    korean,
    bangla="",
    english="",
    category=""
):

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO common_words
        (
            korean,
            bangla,
            english,
            category,
            created_at
        )

        VALUES
        (
            ?, ?, ?, ?, ?
        )
        """,
        (
            korean.strip(),
            bangla.strip(),
            english.strip(),
            category.strip(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()

    conn.close()


# ==========================================
# Search Common Word
# ==========================================

def search_common_word(word):

    conn = get_common_connection()

    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM common_words
        WHERE korean=?
        """,
        (word,)
    )

    row = cur.fetchone()

    conn.close()

    if row:

        return dict(row)

    return None


# ==========================================
# Get All Common Words
# ==========================================

def get_all_common_words():

    conn = get_common_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM common_words
        ORDER BY korean
        """,
        conn
    )

    conn.close()

    return df
# ==========================================
# Update Common Word
# ==========================================

def update_common_word(
    korean,
    bangla="",
    english="",
    category=""
):

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE common_words

        SET
            bangla=?,
            english=?,
            category=?

        WHERE korean=?
        """,
        (
            bangla.strip(),
            english.strip(),
            category.strip(),
            korean.strip()
        )
    )

    conn.commit()

    conn.close()


# ==========================================
# Delete Common Word
# ==========================================

def delete_common_word(word):

    conn = get_common_connection()

    conn.execute(
        """
        DELETE FROM common_words
        WHERE korean=?
        """,
        (word,)
    )

    conn.commit()

    conn.close()


# ==========================================
# Delete All Common Words
# ==========================================

def delete_all_common_words():

    conn = get_common_connection()

    conn.execute(
        """
        DELETE FROM common_words
        """
    )

    conn.commit()

    conn.execute("VACUUM")

    conn.close()


# ==========================================
# Check Common Word
# ==========================================

def is_common_word(word):

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM common_words
        WHERE korean=?
        LIMIT 1
        """,
        (word,)
    )

    found = cur.fetchone() is not None

    conn.close()

    return found
# ==========================================
# Delete All Common Words
# ==========================================

def delete_all_common_words():

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM common_words"
    )

    conn.commit()

    conn.execute("VACUUM")

    conn.close()


# ==========================================
# Duplicate Count
# ==========================================

def common_duplicate_count():

    conn = get_common_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*) FROM
        (
            SELECT korean
            FROM common_words
            GROUP BY korean
            HAVING COUNT(*)>1
        )
        """
    )

    total = cur.fetchone()[0]

    conn.close()

    return total