import sqlite3

DB_PATH = "database/dictionary.db"


def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionary (
            korean TEXT PRIMARY KEY,
            bangla TEXT,
            english TEXT DEFAULT '',
            pos TEXT DEFAULT '',
            topik TEXT DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()


def import_dictionary(df):
    create_table()

    # কমপক্ষে ২টি কলাম থাকতে হবে
    if len(df.columns) < 2:
        raise Exception("Excel/CSV ফাইলে কমপক্ষে ২টি কলাম থাকতে হবে।")

    # প্রথম দুইটি কলাম ব্যবহার করুন
    df = df.iloc[:, :2].copy()
    df.columns = ["Korean", "Bangla"]

    # Header থাকলে বাদ দিন
    header_korean = [
        "korean",
        "korean word",
        "word",
        "코리언 단어",
        "한국어",
        "단어"
    ]

    header_bangla = [
        "bangla",
        "বাংলা",
        "বাংলা অর্থ",
        "bengali",
        "meaning"
    ]

    if len(df) > 0:
        first_korean = str(df.iloc[0]["Korean"]).strip().lower()
        first_bangla = str(df.iloc[0]["Bangla"]).strip().lower()

        if first_korean in header_korean or first_bangla in header_bangla:
            df = df.iloc[1:].reset_index(drop=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    added = 0
    updated = 0
    skipped = 0

    for _, row in df.iterrows():

        korean = str(row["Korean"]).strip()
        bangla = str(row["Bangla"]).strip()

        if korean == "" or korean.lower() == "nan":
            skipped += 1
            continue

        if bangla == "" or bangla.lower() == "nan":
            skipped += 1
            continue

        cursor.execute(
            "SELECT korean FROM dictionary WHERE korean = ?",
            (korean,)
        )

        if cursor.fetchone():

            cursor.execute(
                """
                UPDATE dictionary
                SET bangla = ?
                WHERE korean = ?
                """,
                (bangla, korean)
            )

            updated += 1

        else:

            cursor.execute(
                """
                INSERT INTO dictionary
                (korean, bangla, english, pos, topik)
                VALUES (?, ?, '', '', '')
                """,
                (korean, bangla)
            )

            added += 1

    conn.commit()
    conn.close()

    return added, updated, skipped
