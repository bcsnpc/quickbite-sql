"""
Validate the 10 session queries (Q1-Q9 + Bonus) against the generated CSVs.
Run: python scripts/validate_session_queries.py

Loads CSVs into in-memory SQLite, executes each query, and prints results.
Every query must return non-empty, sensible output.
"""

import os
import sqlite3
import sys

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

TABLES = [
    "cities", "customers", "restaurants", "promotions",
    "orders", "order_items", "ratings",
    "delivery_partners", "delivery_assignments",
]


def load_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    for t in TABLES:
        path = os.path.join(DATA_DIR, f"{t}.csv")
        df = pd.read_csv(path)
        df.to_sql(t, conn, if_exists="replace", index=False)
    return conn


QUERIES = [
    ("Q1: Orders yesterday", """
        SELECT COUNT(*) AS total_orders
        FROM orders
        WHERE order_date = '2026-04-27';
    """),
    ("Q2: Delivered yesterday", """
        SELECT COUNT(*) AS delivered_orders
        FROM orders
        WHERE order_date = '2026-04-27' AND status = 'DELIVERED';
    """),
    ("Q3: Revenue yesterday", """
        SELECT SUM(total_amount) AS revenue
        FROM orders
        WHERE order_date = '2026-04-27' AND status = 'DELIVERED';
    """),
    ("Q4: Revenue by city yesterday", """
        SELECT r.city, ROUND(SUM(o.total_amount), 2) AS revenue
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE o.order_date = '2026-04-27' AND o.status = 'DELIVERED'
        GROUP BY r.city
        ORDER BY revenue DESC;
    """),
    ("Q5: Top 5 restaurants this month", """
        SELECT r.name, r.city, ROUND(SUM(o.total_amount), 2) AS revenue,
               COUNT(*) AS n_orders
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'
        GROUP BY r.name, r.city
        ORDER BY revenue DESC
        LIMIT 5;
    """),
    ("Q6: Customer + restaurant per order yesterday (INNER JOIN)", """
        SELECT c.name AS customer, r.name AS restaurant,
               o.total_amount, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE o.order_date = '2026-04-27'
        LIMIT 10;
    """),
    ("Q7: Customers with no orders in last 30 days (LEFT JOIN)", """
        SELECT c.customer_id, c.name, c.city,
               MAX(o.order_date) AS last_order_date
        FROM customers c
        LEFT JOIN orders o
          ON c.customer_id = o.customer_id
         AND o.order_date >= '2026-03-28'
        GROUP BY c.customer_id, c.name, c.city
        HAVING MAX(o.order_date) IS NULL
        LIMIT 15;
    """),
    ("Q8: Silent churners (CTE)", """
        WITH active_in_jan_feb AS (
            SELECT customer_id, COUNT(*) AS orders_jan_feb
            FROM orders
            WHERE order_date BETWEEN '2026-01-01' AND '2026-02-28'
              AND status = 'DELIVERED'
            GROUP BY customer_id
            HAVING COUNT(*) >= 8
        ),
        active_in_mar_apr AS (
            SELECT DISTINCT customer_id
            FROM orders
            WHERE order_date BETWEEN '2026-03-01' AND '2026-04-27'
              AND status = 'DELIVERED'
        )
        SELECT c.customer_id, c.name, c.city, a.orders_jan_feb
        FROM active_in_jan_feb a
        JOIN customers c ON a.customer_id = c.customer_id
        WHERE a.customer_id NOT IN (SELECT customer_id FROM active_in_mar_apr)
        ORDER BY a.orders_jan_feb DESC
        LIMIT 20;
    """),
    ("Q9: Top cuisine per city this month (window function)", """
        WITH cuisine_revenue AS (
            SELECT r.city, r.cuisine, SUM(o.total_amount) AS revenue
            FROM orders o
            JOIN restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'
            GROUP BY r.city, r.cuisine
        ),
        ranked AS (
            SELECT city, cuisine, revenue,
                   ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rk
            FROM cuisine_revenue
        )
        SELECT city, cuisine, ROUND(revenue, 2) AS revenue
        FROM ranked
        WHERE rk = 1
        ORDER BY revenue DESC;
    """),
    ("Bonus Q: CASE WHEN rating buckets", """
        SELECT CASE
            WHEN r.rating_avg >= 4.5 THEN '4.5+ stars'
            WHEN r.rating_avg >= 4.0 THEN '4.0-4.4 stars'
            WHEN r.rating_avg >= 3.5 THEN '3.5-3.9 stars'
            ELSE 'Below 3.5'
        END AS rating_bucket,
        COUNT(DISTINCT r.restaurant_id) AS n_restaurants,
        ROUND(SUM(o.total_amount), 2) AS revenue,
        ROUND(AVG(o.total_amount), 2) AS avg_order_value
        FROM restaurants r
        LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
            AND o.status = 'DELIVERED'
            AND o.order_date >= '2026-04-01'
        GROUP BY rating_bucket
        ORDER BY revenue DESC;
    """),
]


def main():
    print("Loading CSVs into in-memory SQLite ...")
    conn = load_db()
    print(f"Loaded {len(TABLES)} tables.\n")

    failures = []
    for label, sql in QUERIES:
        print("=" * 70)
        print(label)
        print("=" * 70)
        try:
            df = pd.read_sql_query(sql, conn)
            if df.empty:
                print("  [FAIL] Query returned 0 rows.")
                failures.append(label)
            else:
                print(df.to_string(index=False))
                print(f"\n  rows: {len(df)}")
        except Exception as e:
            print(f"  [ERROR] {e}")
            failures.append(label)
        print()

    conn.close()

    print("=" * 70)
    if failures:
        print(f"FAILED queries ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"All {len(QUERIES)} session queries returned sensible results.")
        sys.exit(0)


if __name__ == "__main__":
    main()
