import sqlite3
import pandas as pd

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_total_words():
    conn = get_connection()

    total = conn.execute(
        "SELECT COUNT(*) FROM dictionary"
    ).fetchone()[0]

    conn.close()

    return total


def get_total_chapters():
    conn = get_connection()

    total = conn.execute(
        """
        SELECT COUNT(DISTINCT chapter)
        FROM dictionary
        WHERE chapter IS NOT NULL
        AND chapter!=''
        """
    ).fetchone()[0]

    conn.close()

    return total


def get_favorite_words():
    conn = get_connection()

    total = conn.execute(
        """
        SELECT COUNT(*)
        FROM dictionary
        WHERE favorite=1
        """
    ).fetchone()[0]

    conn.close()

    return total


def get_recent_words(limit=10):

    conn = get_connection()

    query = """
    SELECT
        korean,
        bangla,
        chapter
    FROM dictionary

    ORDER BY id DESC

    LIMIT ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(limit,)
    )

    conn.close()

    return df


def get_chapter_statistics():

    conn = get_connection()

    query = """
    SELECT
        chapter,
        COUNT(*) AS total
    FROM dictionary

    GROUP BY chapter

    ORDER BY chapter
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df