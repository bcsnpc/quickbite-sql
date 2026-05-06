"""
Build a local SQLite database (quickbite.db) from the CSVs in data/.
Use this when you don't want Colab — load it in DBeaver, run queries from
the command line via `sqlite3 quickbite.db`, or use it from any Python script.

Run: python scripts/load_to_sqlite.py
"""

import os
import sqlite3
import sys

import pandas as pd

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DB_PATH  = os.path.join(ROOT, "quickbite.db")

TABLES = [
    "cities", "customers", "restaurants", "promotions",
    "orders", "order_items", "ratings",
    "delivery_partners", "delivery_assignments",
]


def main():
    if not os.path.isdir(DATA_DIR):
        print(f"ERROR: data directory not found at {DATA_DIR}")
        print("Run `python scripts/generate_data.py` first.")
        sys.exit(1)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    print(f"Building {DB_PATH} ...")

    for t in TABLES:
        csv_path = os.path.join(DATA_DIR, f"{t}.csv")
        if not os.path.exists(csv_path):
            print(f"  WARN: {csv_path} not found, skipping")
            continue
        df = pd.read_csv(csv_path)
        df.to_sql(t, conn, if_exists="replace", index=False)
        print(f"  {t:<22} {len(df):>8,} rows")

    # Useful indexes for the session queries
    cur = conn.cursor()
    cur.executescript("""
        CREATE INDEX IF NOT EXISTS idx_orders_date          ON orders(order_date);
        CREATE INDEX IF NOT EXISTS idx_orders_customer      ON orders(customer_id);
        CREATE INDEX IF NOT EXISTS idx_orders_restaurant    ON orders(restaurant_id);
        CREATE INDEX IF NOT EXISTS idx_orders_status        ON orders(status);
        CREATE INDEX IF NOT EXISTS idx_ratings_order        ON ratings(order_id);
        CREATE INDEX IF NOT EXISTS idx_assignments_partner  ON delivery_assignments(partner_id);
        CREATE INDEX IF NOT EXISTS idx_order_items_order    ON order_items(order_id);
    """)
    conn.commit()
    conn.close()

    size_mb = os.path.getsize(DB_PATH) / 1024 / 1024
    print(f"\nDone. Database size: {size_mb:.1f} MB")
    print(f"Open in DBeaver:        File > New > Database Connection > SQLite > browse to {DB_PATH}")
    print(f"Quick CLI test:         sqlite3 {DB_PATH} \"SELECT COUNT(*) FROM orders;\"")


if __name__ == "__main__":
    main()
