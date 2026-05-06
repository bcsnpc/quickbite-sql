"""
Execute every statement in solutions/all_solutions.sql against the generated CSVs
and confirm each returns a non-empty, error-free result.

Run: python scripts/run_all_solutions.py
"""

import os
import re
import sqlite3
import sys

import pandas as pd

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SQL_FILE = os.path.join(ROOT, "solutions", "all_solutions.sql")

TABLES = [
    "cities", "customers", "restaurants", "promotions",
    "orders", "order_items", "ratings",
    "delivery_partners", "delivery_assignments",
]


def load_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    for t in TABLES:
        df = pd.read_csv(os.path.join(DATA_DIR, f"{t}.csv"))
        df.to_sql(t, conn, if_exists="replace", index=False)
    return conn


def split_solutions(sql_text: str) -> list:
    """
    Split the file into (label, sql) tuples by splitting on the
    `-- =====` block headers that mark each solution.
    """
    blocks = re.split(r"^-- ={5,}\s*$", sql_text, flags=re.MULTILINE)
    pairs = []
    label = None
    for chunk in blocks:
        chunk = chunk.strip()
        if not chunk:
            continue
        # Header blocks look like: "-- BEGINNER 1: ..." possibly with surrounding lines
        header_lines = [
            ln for ln in chunk.splitlines()
            if ln.strip().startswith("--")
            and re.search(r"\b(BEGINNER|INTERMEDIATE|ADVANCED|BONUS)\b\s+\d+", ln)
        ]
        if header_lines:
            label = header_lines[0].lstrip("- ").strip()
            continue
        if chunk.startswith("--"):
            # Top-of-file banner — skip
            continue
        if label and chunk:
            # Take only SQL up to the trailing semicolon block
            pairs.append((label, chunk.rstrip(";\n ") + ";"))
            label = None
    return pairs


def main():
    with open(SQL_FILE, encoding="utf-8") as f:
        text = f.read()

    pairs = split_solutions(text)
    print(f"Found {len(pairs)} solutions in {SQL_FILE}\n")

    conn = load_db()

    failed, empty = [], []
    for label, sql in pairs:
        try:
            df = pd.read_sql_query(sql, conn)
        except Exception as e:
            print(f"[FAIL] {label}\n        {e}\n")
            failed.append(label)
            continue

        n = len(df)
        if n == 0:
            print(f"[EMPTY] {label}  (0 rows returned)")
            empty.append(label)
        else:
            sample = df.head(1).to_dict(orient="records")[0]
            sample_str = ", ".join(f"{k}={v}" for k, v in list(sample.items())[:3])
            print(f"[ OK ] {label:<60} rows={n:>4}   first: {sample_str}")

    conn.close()

    print()
    if failed:
        print(f"FAILED: {len(failed)}")
        for f in failed:
            print(f"  - {f}")
    if empty:
        print(f"EMPTY: {len(empty)}")
        for f in empty:
            print(f"  - {f}")
    if not failed and not empty:
        print(f"All {len(pairs)} solutions executed cleanly with non-empty results.")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
