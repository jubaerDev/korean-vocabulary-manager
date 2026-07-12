import pandas as pd
from io import BytesIO

def export_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Words")

    return output.getvalue()


def export_csv(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def export_txt(df):
    return "\n".join(df["Word"])