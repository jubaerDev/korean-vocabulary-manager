import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


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


def get_words(chapter):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            korean,
            bangla
        FROM dictionary
        WHERE chapter=?
        """,
        conn,
        params=(chapter,)
    )

    conn.close()

    return df