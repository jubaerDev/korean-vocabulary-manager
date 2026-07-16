import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"


def get_connection():

    return sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )


# ==========================================
# Get Chapter List
# ==========================================

def get_chapters():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT DISTINCT chapter
        FROM dictionary
        ORDER BY chapter
        """,
        conn
    )

    conn.close()

    return df["chapter"].tolist()


# ==========================================
# Load Chapter Words
# ==========================================

def get_words_by_chapter(chapter):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            korean,
            bangla
        FROM dictionary
        WHERE chapter=?
        ORDER BY korean
        """,
        conn,
        params=(chapter,)
    )

    conn.close()

    return df