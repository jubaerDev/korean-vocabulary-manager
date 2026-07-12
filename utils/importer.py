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

    # কমপক্ষে ২টি কলাম থাকতে হবে
    if len(df.columns) < 2:
        raise Exception("Excel/CSV ফাইলে কমপক্ষে ২টি কলাম থাকতে হবে।")

    # শুধুমাত্র প্রথম দুইটি কলাম নিন
    df = df.iloc[:, :2].copy()

    # কলামের নাম নির্দিষ্ট করুন
    df.columns = ["Korean", "Bangla"]

    # Header চিনতে ব্যবহৃত তালিকা
    korean_headers = [
        "korean",
        "korean word",
        "word",
        "한국어",
        "코리언 단어",
        "단어"
    ]

    bangla_headers = [
        "bangla",
        "বাংলা",
        "বাংলা অর্থ",
        "bengali",
        "meaning"
    ]

    # প্রথম Row Header কিনা পরীক্ষা
    if len(df) > 0:

        first_korean = str(df.iloc[0]["Korean"]).strip().lower()
        first_bangla = str(df.iloc[0]["Bangla"]).strip().lower()

        if first_korean in korean_headers or first_bangla in bangla_headers:
            df = df.iloc[1:].reset_index(drop=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    added = 0
    updated = 0
    skipped = 0

    for _, row in df.iterrows():

        korean = str(row["Korean"]).strip()
        bangla = str(row["Bangla"]).strip()

        # ফাঁকা Row বাদ দিন
        if korean == "" or korean.lower() == "nan":
            skipped += 1
            continue

        if bangla == "" or bangla.lower() == "nan":
            skipped += 1
            continue

        # আগে থেকেই আছে কিনা দেখুন
        cur.execute(
            "SELECT korean FROM dictionary WHERE korean=?",
            (korean,)
        )

        if cur.fetchone():

            cur.execute("""
                UPDATE dictionary
                SET bangla=?
                WHERE korean=?
            """, (bangla, korean))

            updated += 1

        else:

            cur.execute("""
                INSERT INTO dictionary
                (korean, bangla, english, pos, topik)
                VALUES (?, ?, '', '', '')
            """, (korean, bangla))

            added += 1

    conn.commit()
    conn.close()

    return added, updated, skipped            VALUES(?,?,?,?,?)
            """,
            (korean, bangla, english, pos, topik))

            added += 1

    conn.commit()
    conn.close()

    return added, updated, skipped
