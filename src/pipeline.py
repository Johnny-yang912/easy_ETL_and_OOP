from __future__ import annotations
from pathlib import Path
import pandas as pd
import sqlite3, csv
from transformers.time_bucket import TimeBucketTransformer

def extract(src_csv: str, raw_csv: str) -> str:
    Path(raw_csv).parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(src_csv)
    df.to_csv(raw_csv, index=False)
    print(f"Data extracted to {raw_csv}")
    return raw_csv

def transform(raw_csv: str, out_csv: str, datetime_col: str = "ts") -> str:
    df = pd.read_csv(raw_csv)
    t = TimeBucketTransformer(use_cols=[datetime_col]).fit(df)
    df_out = t.transform(df)
    df_out.to_csv(out_csv, index=False)
    print(f"Data transformed and saved to {out_csv}")
    return out_csv

def load(in_csv: str, sqlite_path: str, table: str = "data") -> None:
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data(
          txn_id TEXT, ts TEXT, amount REAL, category TEXT, user_id TEXT,
          region TEXT, status TEXT, method TEXT, discount REAL, remarks TEXT,
          hour INTEGER
        )
    """)
    # 明確指定欄位順序，避免 CSV 欄位順序變動
    rows = []
    with open(in_csv, "r") as f:
        dr = csv.DictReader(f)
        for i in dr:
            rows.append((
                i["txn_id"], i["ts"], i["amount"], i["category"], i["user_id"],
                i["region"], i["status"], i["method"], i["discount"], i["remarks"],
                i["hour"]
            ))
    cur.executemany("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit(); conn.close()
    print(f"Data loaded into database at {sqlite_path}")

def run_pipeline(
    src_csv: str,
    raw_csv: str,
    out_csv: str,
    sqlite_path: str,
    table: str = "data",
    datetime_col: str = "ts",
) -> dict:
    raw = extract(src_csv, raw_csv)
    new = transform(raw, out_csv, datetime_col=datetime_col)
    load(new, sqlite_path, table)
    df = pd.read_csv(new)
    return {
        "rows": len(df),
        "cols": list(df.columns),
        "raw_csv": raw,
        "out_csv": new,
        "sqlite_path": sqlite_path,
        "table": table,
    }
