import sqlite3

DB_PATH = "database/dictionary.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def search_word(word):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM dictionary
        WHERE korean=?
        """,
        (word,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


def increase_search_count(word):

    conn = get_connection()

    conn.execute(
        """
        UPDATE dictionary
        SET search_count = search_count + 1
        WHERE korean=?
        """,
        (word,)
    )

    conn.commit()
    conn.close()