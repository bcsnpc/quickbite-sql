# Run QuickBite SQL locally

Three options, depending on what you've already got installed. Pick one.

| If you want | Use | Setup time |
|---|---|---|
| GUI to click around tables | **SQLite + DBeaver** (or DB Browser for SQLite) | ~3 min |
| Single-binary, no setup, query CSVs directly | **DuckDB** | ~1 min |
| The same engine you use at work | **PostgreSQL** | ~10 min |

Prerequisite for all three: **clone the repo** and have the `data/` folder. If `data/` is empty, run `python scripts/generate_data.py` to populate it.

---

## A. SQLite + DBeaver

### 1. Build the database

```bash
python scripts/load_to_sqlite.py
```

This produces `quickbite.db` in the repo root (~43 MB) and adds useful indexes.

### 2. Open it in DBeaver

1. Install DBeaver Community Edition: <https://dbeaver.io/download/>
2. Launch DBeaver.
3. **File → New → Database Connection → SQLite → Next**.
4. Click **Browse** and select `quickbite.db`.
5. Click **Test Connection** (it'll prompt to download the SQLite driver — accept).
6. **Finish.**
7. Expand the connection in the left pane → **Databases → Tables**. You'll see all 9 tables.
8. Double-click any table to view rows. Or right-click → **SQL Editor** to write queries.

### 3. Quick smoke test

In the SQL editor, run:

```sql
SELECT COUNT(*) FROM orders;
-- expect ~106,414
```

> **Alternative GUI:** [DB Browser for SQLite](https://sqlitebrowser.org/) is lighter and just as good for this dataset.

### 4. CLI alternative

If you prefer the terminal:

```bash
sqlite3 quickbite.db
sqlite> SELECT city, COUNT(*) FROM restaurants GROUP BY city;
sqlite> .quit
```

---

## B. DuckDB — query CSVs directly, no loading

DuckDB can run SQL straight against the CSV files — no database file, no schema, no `COPY FROM`.

### 1. Install

```bash
pip install duckdb
```

…or the standalone CLI from <https://duckdb.org/docs/installation/>.

### 2. Query CSVs directly

```bash
cd quickbite-sql
duckdb
```

```sql
-- These work without any LOAD step. DuckDB infers schema from the CSV header.
SELECT * FROM 'data/orders.csv' LIMIT 10;

SELECT status, COUNT(*) AS n
FROM 'data/orders.csv'
GROUP BY status;
```

### 3. Optional: register the CSVs as views

If you'd rather write `FROM orders` than `FROM 'data/orders.csv'`:

```sql
CREATE VIEW orders               AS SELECT * FROM 'data/orders.csv';
CREATE VIEW customers            AS SELECT * FROM 'data/customers.csv';
CREATE VIEW restaurants          AS SELECT * FROM 'data/restaurants.csv';
CREATE VIEW order_items          AS SELECT * FROM 'data/order_items.csv';
CREATE VIEW ratings              AS SELECT * FROM 'data/ratings.csv';
CREATE VIEW cities               AS SELECT * FROM 'data/cities.csv';
CREATE VIEW promotions           AS SELECT * FROM 'data/promotions.csv';
CREATE VIEW delivery_partners    AS SELECT * FROM 'data/delivery_partners.csv';
CREATE VIEW delivery_assignments AS SELECT * FROM 'data/delivery_assignments.csv';
```

Now the session queries from the notebook work unchanged:

```sql
SELECT COUNT(*) AS total_orders
FROM orders
WHERE order_date = '2026-04-27';
```

> The window functions and CTEs in the notebook all work in DuckDB.
> One nuance: DuckDB types dates as `DATE`, not `TEXT` like SQLite — but the queries written for SQLite still work because DuckDB auto-converts string literals.

---

## C. PostgreSQL

### 1. Create the database

```bash
createdb quickbite
```

### 2. Build the schema

```bash
psql quickbite -f scripts/schema.sql
```

This drops + recreates all 9 tables with proper foreign keys.

### 3. Load each CSV

The fastest way is `\copy` from the psql shell (works with relative paths from your shell, unlike `COPY FROM` which expects server-side paths):

```bash
psql quickbite
```

```
\copy cities                FROM 'data/cities.csv'                WITH CSV HEADER
\copy customers             FROM 'data/customers.csv'             WITH CSV HEADER
\copy restaurants           FROM 'data/restaurants.csv'           WITH CSV HEADER
\copy promotions            FROM 'data/promotions.csv'            WITH CSV HEADER
\copy orders                FROM 'data/orders.csv'                WITH CSV HEADER
\copy order_items           FROM 'data/order_items.csv'           WITH CSV HEADER
\copy ratings               FROM 'data/ratings.csv'               WITH CSV HEADER
\copy delivery_partners     FROM 'data/delivery_partners.csv'     WITH CSV HEADER
\copy delivery_assignments  FROM 'data/delivery_assignments.csv'  WITH CSV HEADER
```

> Order matters because of foreign keys — load `cities → customers/restaurants/promotions → orders → order_items/ratings → delivery_partners → delivery_assignments` in roughly the order above.

### 4. Verify

```sql
SELECT COUNT(*) FROM orders;
-- expect ~106,414

SELECT COUNT(*) FROM delivery_assignments;
-- expect ~97,831
```

### 5. Notes on Postgres-specific syntax

The session queries are written for SQLite, which is the lowest common denominator. Two functions differ in Postgres:

| SQLite | PostgreSQL equivalent |
|---|---|
| `julianday(d2) - julianday(d1)` | `(d2::date - d1::date)` (returns days as integer) |
| `(JULIANDAY(t2) - JULIANDAY(t1)) * 1440` | `EXTRACT(EPOCH FROM (t2::timestamp - t1::timestamp)) / 60` |
| `SUBSTR(order_date, 1, 7)` | `TO_CHAR(order_date, 'YYYY-MM')` |

Everything else (`WITH`, `JOIN`, `GROUP BY`, `ROW_NUMBER() OVER`, `CASE WHEN`) is identical.

---

## Smoke test for any of the three

After your environment is set up, run **Q1** from the notebook:

```sql
SELECT COUNT(*) AS total_orders
FROM orders
WHERE order_date = '2026-04-27';
-- expect 900
```

If you get `900`, you're set. Open the notebook (`notebook/QuickBite_SQL_Story.ipynb`) on GitHub to read along, but execute the queries in your local environment.
