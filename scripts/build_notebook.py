"""
Build notebook/QuickBite_SQL_Story.ipynb programmatically.
Run: python scripts/build_notebook.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "notebook", "QuickBite_SQL_Story.ipynb")

cells = []


def _next_id() -> str:
    return f"cell-{len(cells):04d}"


def md(text: str) -> None:
    cells.append({
        "id": _next_id(),
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True) if "\n" in text else [text],
    })


def code(text: str) -> None:
    cells.append({
        "id": _next_id(),
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True) if "\n" in text else [text],
    })


# ─── Cell 1: title + hook ────────────────────────────────────────────────────

md("""# QuickBite SQL — Learn SQL Through a Story

You're the new data analyst at **QuickBite**, a food delivery startup operating in 8 Indian cities.
Today is **2026-04-28**. The CEO, Priya, walks up to your desk and asks 9 questions over the next hour.
Each question forces you to learn one new piece of SQL.

By the end of this notebook you'll have used: `SELECT`, `WHERE`, `COUNT/SUM/AVG`, `GROUP BY`,
`INNER JOIN`, `LEFT JOIN`, `CTEs`, window functions, and `CASE WHEN`. Nine concepts in nine queries.

## The dataset

| Table | Rows | What it holds |
|---|---|---|
| `customers` | 10,000 | Who orders the food |
| `restaurants` | 200 | Who cooks it |
| `orders` | ~106K | Each order: customer, restaurant, amount, status |
| `order_items` | ~265K | Line items per order (dish, quantity, price) |
| `ratings` | ~66K | Star reviews on delivered orders |
| `delivery_partners` | 500 | Who delivers (bike/scooter/bicycle) |
| `cities`, `promotions`, `delivery_assignments` | bonus tables for practice |

## How to use this notebook

1. Run **Cell 3** (the setup cell) — it downloads the data and loads it into SQLite. Takes ~30 seconds.
2. Read each markdown cell, then run the SQL cell below it. The output appears immediately.
3. Try the **💪 try this** mini-exercises in each Act. Solutions are at the bottom.
4. Don't skip the "📖 Explain in English" lines — they translate the SQL back to plain words.

> Currency throughout: **₹ (Indian Rupees)**. All dates are ISO format (`YYYY-MM-DD`).
""")

# ─── Cell 2: setup heading ──────────────────────────────────────────────────

md("""## 🛠️ Setup — run this first

The cell below does four things:
1. Installs the SQL magic for Jupyter
2. Downloads the 9 CSV files from GitHub
3. Loads them into a local SQLite database
4. Connects the SQL magic so you can write `%%sql` in any cell

**Run it once and wait for the** `✓ Ready` **message.** Re-running is safe.
""")

# ─── Cell 3: setup code ─────────────────────────────────────────────────────

code("""# Install SQL magic (silent)
!pip install -q jupysql sqlalchemy

import os
import pandas as pd
import sqlite3

GITHUB_USER = "bcsnpc"
BRANCH      = "main"
BASE_URL    = f"https://raw.githubusercontent.com/{GITHUB_USER}/quickbite-sql/{BRANCH}/data"

TABLES = [
    "cities", "customers", "restaurants", "promotions",
    "orders", "order_items", "ratings",
    "delivery_partners", "delivery_assignments",
]

DB_PATH = "/content/quickbite.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)

print("Downloading CSVs and loading into SQLite ...")
for t in TABLES:
    url = f"{BASE_URL}/{t}.csv"
    df = pd.read_csv(url)
    df.to_sql(t, conn, if_exists="replace", index=False)
    print(f"  {t:<22} {len(df):>8,} rows")

conn.commit()
conn.close()

# Connect SQL magic
%load_ext sql
%sql sqlite:////content/quickbite.db

# Show all rows (default cap is 10) and render results as pandas DataFrames
# (Colab applies its interactive table widget automatically).
%config SqlMagic.displaylimit = None
%config SqlMagic.autopandas = True

print("\\n✓ Ready. You can now run %%sql cells against the database.")
""")

# ─── Cells 4-13: Peek at the 5 main tables ─────────────────────────────────

PEEK_TABLES = [
    ("customers",    "10,000 customer records — who orders our food."),
    ("restaurants",  "200 restaurants across 8 cities, with average rating and price tier."),
    ("orders",       "Every order placed: customer, restaurant, amount, status, payment method."),
    ("order_items",  "What was in each order. One row per dish."),
    ("ratings",      "Star reviews customers leave on delivered orders."),
]

for tname, blurb in PEEK_TABLES:
    md(f"""### Peek: `{tname}`

{blurb}
""")
    code(f"""%%sql
SELECT * FROM {tname} LIMIT 5;
""")

# ─── Act 1: Simple Questions (Q1, Q2, Q3) ──────────────────────────────────

md("""---
# 🎬 Act 1 — Priya asks: "How did we do yesterday?"

Yesterday is **2026-04-27**. Priya wants three numbers, fast.

**You'll learn:** `SELECT`, `FROM`, `WHERE`, `COUNT`, `SUM`.
The mental model: SQL is just a way of asking questions of a table.
""")

md("""## Q1 — How many orders did we get yesterday?

📖 **Explain in English:** Count every row in the `orders` table where the `order_date` equals `'2026-04-27'`.
""")

code("""%%sql
SELECT COUNT(*) AS total_orders
FROM orders
WHERE order_date = '2026-04-27';
""")

md("""## Q2 — How many of those were actually delivered?

Some orders are cancelled or refunded. Priya only cares about the delivered ones.

📖 **Explain in English:** Same as Q1, but add a second filter: status must be `'DELIVERED'`.
""")

code("""%%sql
SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE order_date = '2026-04-27'
  AND status = 'DELIVERED';
""")

md("""## Q3 — How much money did we make yesterday?

📖 **Explain in English:** Add up the `total_amount` of every delivered order from yesterday.
The `SUM` function adds a column; `COUNT` counts rows.
""")

code("""%%sql
SELECT SUM(total_amount) AS revenue_inr
FROM orders
WHERE order_date = '2026-04-27'
  AND status = 'DELIVERED';
""")

md("""### 💪 Try this — Act 1 mini-exercises

1. How many orders were **CANCELLED** yesterday? (Hint: change the status filter)
2. How many orders happened on **2026-04-26**? (Two days ago)
3. What was the **average** order value yesterday for delivered orders? (Hint: `AVG(total_amount)`)

> 🛠 Modify the queries above and re-run. Solutions are at the bottom of the notebook.
""")

# ─── Act 2: Grouping (Q4, Q5) ───────────────────────────────────────────────

md("""---
# 🎬 Act 2 — Priya asks: "Break it down by city. And which restaurants are killing it this month?"

One number per city. Then the top 5 restaurants for the whole month.

**You'll learn:** `GROUP BY`, `ORDER BY`, `LIMIT`, and your first `JOIN`.
The mental model for `GROUP BY`: collapse rows that share a value into a single row, then aggregate.
The mental model for `JOIN`: tables hold hands by an `id` column.
""")

md("""## Q4 — Revenue by city yesterday

We need each city's revenue. But the `orders` table doesn't have a `city` column —
the city lives on the `restaurants` table. So we **join** the two tables on `restaurant_id`.

📖 **Explain in English:** Take orders, attach each one to its restaurant (so we know the city),
keep only delivered orders from yesterday, group by city, sum the revenue, sort highest first.
""")

code("""%%sql
SELECT r.city,
       ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_date = '2026-04-27'
  AND o.status = 'DELIVERED'
GROUP BY r.city
ORDER BY revenue DESC;
""")

md("""## Q5 — Top 5 restaurants by revenue this month

Same shape, but group by restaurant instead of city, and limit to 5.

📖 **Explain in English:** Per restaurant in April, sum up the revenue from delivered orders.
Sort highest first. Show the top 5.
""")

code("""%%sql
SELECT r.name,
       r.city,
       ROUND(SUM(o.total_amount), 2) AS revenue,
       COUNT(*)                       AS n_orders
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_date >= '2026-04-01'
  AND o.status = 'DELIVERED'
GROUP BY r.name, r.city
ORDER BY revenue DESC
LIMIT 5;
""")

md("""### 💪 Try this — Act 2 mini-exercises

1. **Orders per cuisine** this month (delivered only). Group by `r.cuisine`.
2. **Revenue per payment method** yesterday. Group by `payment_method`.
3. **Bottom 5 restaurants** by revenue this month. Same query as Q5 with `ORDER BY revenue ASC`.

> Tip: when you change a `GROUP BY` column, change the `SELECT` columns to match.
""")

# ─── Act 3: Joins (Q6, Q7) ─────────────────────────────────────────────────

md("""---
# 🎬 Act 3 — Marketing wants names. And: "Who hasn't ordered in a month?"

Marketing wants a human-readable list of yesterday's orders — customer name, restaurant name, amount.
Then they want a re-engagement list: customers who've gone silent in the last 30 days.

**You'll learn:** the difference between `INNER JOIN` and `LEFT JOIN`.

| | Mental model |
|---|---|
| **INNER JOIN** | Only rows where the match exists in **both** tables. Drops anything unmatched. |
| **LEFT JOIN**  | Keep **every** row from the left table. If no match on the right, fill with `NULL`. |

The "find an absence" pattern uses LEFT JOIN: keep all customers, attach their orders if they have any —
then filter to the rows where the order side came up `NULL`.
""")

md("""## Q6 — Customer + restaurant per order yesterday (INNER JOIN)

Three tables: `orders` is the spine, `customers` gives us the customer name, `restaurants` gives us the restaurant name.

📖 **Explain in English:** For every order yesterday, look up its customer name and its restaurant name,
and show those alongside the amount and status.
""")

code("""%%sql
SELECT c.name AS customer,
       r.name AS restaurant,
       o.total_amount,
       o.status
FROM orders o
JOIN customers   c ON o.customer_id   = c.customer_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_date = '2026-04-27'
LIMIT 10;
""")

md("""## Q7 — Customers with **zero** orders in the last 30 days (LEFT JOIN)

The trick: if you `INNER JOIN` customers to orders, you lose the customers who never ordered —
those are exactly the ones marketing wants. Use `LEFT JOIN` to keep all customers, then
filter to the ones whose joined order side is `NULL`.

📖 **Explain in English:** Start with every customer. Attach their orders from the last 30 days, if any.
Group by customer. Keep only the ones where the maximum order date is `NULL` —
meaning they had no orders in the window at all.
""")

code("""%%sql
SELECT c.customer_id,
       c.name,
       c.city,
       MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o
       ON c.customer_id = o.customer_id
      AND o.order_date >= '2026-03-28'
GROUP BY c.customer_id, c.name, c.city
HAVING MAX(o.order_date) IS NULL
LIMIT 15;
""")

md("""### 🧠 `WHERE` vs `HAVING` — the timing rule

- `WHERE` filters rows **before** they're grouped.
- `HAVING` filters groups **after** aggregation.

You can't use `HAVING MAX(...)` in a `WHERE` clause — `WHERE` runs too early.

### 💪 Try this — Act 3 mini-exercises

1. Show the **5 most expensive orders** placed yesterday, with the customer name. (INNER JOIN + ORDER BY)
2. Customers who have **never** placed any order at all. (LEFT JOIN with no date filter)
3. Restaurants that have **never received an order**. (LEFT JOIN restaurants → orders, find NULLs)
""")

# ─── Act 4: CTEs (Q8) ──────────────────────────────────────────────────────

md("""---
# 🎬 Act 4 — Priya asks: "Who are our silent churners?"

A **silent churner** is a customer who:
- Was active in **Jan-Feb** (≥ 8 delivered orders)
- Has **zero orders** in **Mar-Apr**

So: a list, minus another list. Two named sub-questions, then combined.

**You'll learn:** **CTEs** (Common Table Expressions, the `WITH` clause).
CTEs are not advanced — they're a way to make queries **readable**.
You break the question into named steps and stack them.

### How to read this in three English sentences before looking at the SQL:

1. Find customers who placed ≥ 8 delivered orders in **Jan-Feb**. Call this list **A**.
2. Find customers who placed any delivered order in **Mar-Apr**. Call this list **B**.
3. Return everyone in **A** who is **not** in **B**, with their name and city.

That's exactly the shape of the query below.
""")

md("""## Q8 — Silent churners

📖 **Explain in English:** Build list A (active in Jan-Feb), build list B (active in Mar-Apr),
then keep only the people who are in A but not in B. Order by their Jan-Feb activity, top 20.
""")

code("""%%sql
WITH active_in_jan_feb AS (
    SELECT customer_id,
           COUNT(*) AS orders_jan_feb
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
SELECT c.customer_id,
       c.name,
       c.city,
       a.orders_jan_feb
FROM active_in_jan_feb a
JOIN customers c ON a.customer_id = c.customer_id
WHERE a.customer_id NOT IN (SELECT customer_id FROM active_in_mar_apr)
ORDER BY a.orders_jan_feb DESC
LIMIT 20;
""")

md("""### 💪 Try this — Act 4 mini-exercises

1. Modify Q8: instead of "no orders in Mar-Apr", find customers whose **Mar-Apr orders dropped by half**
   compared to Jan-Feb. (Hint: build both counts as CTEs and compare.)
2. Find restaurants that **gained** customers in Mar-Apr vs Jan-Feb. Two CTEs, then a join.
3. Build a CTE called `april_revenue` that gives revenue per restaurant in April,
   then list the top 10 from it.
""")

# ─── Act 5: Window functions (Q9) ───────────────────────────────────────────

md("""---
# 🎬 Act 5 — Priya asks: "What's the top cuisine in each city this month?"

Sounds simple. But "the top one **in each city**" needs a special SQL feature.

If you just `GROUP BY city, cuisine` and `ORDER BY revenue DESC`, you get the top cuisine **overall** —
not the top per city. You need to rank within each city, then keep rank = 1.

**You'll learn:** **window functions**, specifically `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`.

The mental model:
> `PARTITION BY city` = "do the ranking **separately for each city**, but **don't merge** the rows."
> Unlike `GROUP BY`, the original rows are preserved — you just get an extra column with the rank.
""")

md("""## Q9 — Top cuisine per city this month

📖 **Explain in English:** Build cuisine revenue per city. Number them within each city, highest first.
Keep only the rows where the number is 1.
""")

code("""%%sql
WITH cuisine_revenue AS (
    SELECT r.city,
           r.cuisine,
           SUM(o.total_amount) AS revenue
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    WHERE o.order_date >= '2026-04-01'
      AND o.status = 'DELIVERED'
    GROUP BY r.city, r.cuisine
),
ranked AS (
    SELECT city,
           cuisine,
           revenue,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rk
    FROM cuisine_revenue
)
SELECT city,
       cuisine,
       ROUND(revenue, 2) AS revenue
FROM ranked
WHERE rk = 1
ORDER BY revenue DESC;
""")

md("""### Ranking variations — pick the right one

| Function | Behavior on ties |
|---|---|
| `ROW_NUMBER()`  | Always unique. Ties get arbitrary order: 1, 2, 3, 4. |
| `RANK()`        | Ties share rank, leaves gaps: 1, 2, 2, 4. |
| `DENSE_RANK()`  | Ties share rank, no gaps: 1, 2, 2, 3. |
| `LAG(col)`      | Look at the **previous** row's value (in the partition). |
| `LEAD(col)`     | Look at the **next** row's value. |

### 💪 Try this — Act 5 mini-exercises

1. Top **3** restaurants per city this month (change `WHERE rk = 1` to `WHERE rk <= 3`).
2. For each customer's orders, show the **previous** order amount using `LAG(total_amount)`.
3. Use `RANK()` instead of `ROW_NUMBER()` and see whether any city has tied cuisines.
""")

# ─── Bonus: CASE WHEN ──────────────────────────────────────────────────────

md("""---
# 🎁 Bonus — `CASE WHEN`: bucketing values

Sometimes you want to group continuous values (like `rating_avg`) into named buckets.
That's what `CASE WHEN` does — it's the SQL equivalent of `if/elif/else`.

📖 **Explain in English:** For every restaurant, label it with a rating bucket.
Attach its April delivered orders. Group by bucket. Show how many restaurants and how much revenue per bucket.
""")

code("""%%sql
SELECT CASE
           WHEN r.rating_avg >= 4.5 THEN '4.5+ stars'
           WHEN r.rating_avg >= 4.0 THEN '4.0-4.4 stars'
           WHEN r.rating_avg >= 3.5 THEN '3.5-3.9 stars'
           ELSE 'Below 3.5'
       END                                       AS rating_bucket,
       COUNT(DISTINCT r.restaurant_id)           AS n_restaurants,
       ROUND(SUM(o.total_amount), 2)             AS revenue,
       ROUND(AVG(o.total_amount), 2)             AS avg_order_value
FROM restaurants r
LEFT JOIN orders o
       ON r.restaurant_id = o.restaurant_id
      AND o.status = 'DELIVERED'
      AND o.order_date >= '2026-04-01'
GROUP BY rating_bucket
ORDER BY revenue DESC;
""")

# ─── What you actually learned ─────────────────────────────────────────────

md("""---
# 🎓 What you actually learned

In one hour you used **9 SQL concepts** to answer 9 real business questions:

1. **`SELECT … FROM`** — pick columns from a table
2. **`WHERE`** — filter rows
3. **`COUNT / SUM / AVG`** — aggregate functions
4. **`GROUP BY`** — collapse rows that share a value
5. **`ORDER BY` + `LIMIT`** — sort and trim
6. **`INNER JOIN`** — combine two tables on a shared key
7. **`LEFT JOIN`** — keep all rows from the left side, even unmatched ones
8. **CTEs (`WITH`)** — break a query into named steps
9. **Window functions (`OVER PARTITION BY`)** — rank or compare within groups

Plus a bonus: **`CASE WHEN`** for bucketing.

> SQL isn't a language you memorize — it's a way of asking questions of a table.
> The more questions you ask, the more fluent you become.
""")

# ─── Inline cheatsheet ─────────────────────────────────────────────────────

md("""---
# 📋 Quick cheatsheet

### Query skeleton

```sql
SELECT  col1, AGG(col2)         -- what to show
FROM    table_a a
JOIN    table_b b ON a.id = b.a_id
WHERE   col1 = 'value'           -- filter rows BEFORE grouping
GROUP BY col1
HAVING  AGG(col2) > 100          -- filter groups AFTER aggregation
ORDER BY AGG(col2) DESC
LIMIT 10;
```

### Aggregates

| Function | Returns |
|---|---|
| `COUNT(*)` | Number of rows |
| `COUNT(DISTINCT col)` | Number of unique values |
| `SUM(col)` | Total |
| `AVG(col)` | Mean |
| `MIN(col)` / `MAX(col)` | Extremes |

### Joins (mental model)

| | What you keep |
|---|---|
| `INNER JOIN` | Only rows that match in **both** tables |
| `LEFT JOIN`  | All rows from **left** table; unmatched right side becomes `NULL` |
| `RIGHT JOIN` | All rows from **right** table (rarely needed) |
| `FULL OUTER` | All rows from both, `NULL` where unmatched |

### CTEs

```sql
WITH step1 AS (SELECT … FROM …),
     step2 AS (SELECT … FROM step1)
SELECT * FROM step2;
```

### Window functions

```sql
ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC)
```

### Useful patterns

- **Top N per group**: `ROW_NUMBER() OVER (PARTITION BY group ORDER BY metric DESC) <= N`
- **Find absences**: `LEFT JOIN ... WHERE right.col IS NULL`
- **% of total**: `metric * 100.0 / SUM(metric) OVER ()`
""")

# ─── Practice exercises (15) ────────────────────────────────────────────────

md("""---
# 🏋️ Practice exercises

15 problems, organized from easy to hard. Try each one before peeking at the solutions.

> The solutions are in the cells **after** these. Each solution is in its own code cell, so you can run it.
""")

EXERCISES = [
    # (title, description, solution_sql)
    ("E1 — Customers signed up in 2025",
     "Count customers whose `signup_date` is in 2025.",
     """SELECT COUNT(*) AS n_customers
FROM customers
WHERE signup_date >= '2025-01-01' AND signup_date < '2026-01-01';"""),

    ("E2 — Average order value this month",
     "Among delivered orders in April 2026, what's the average `total_amount`?",
     """SELECT ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE order_date >= '2026-04-01' AND status = 'DELIVERED';"""),

    ("E3 — Top 10 most expensive orders",
     "Show the 10 single orders with the highest `total_amount` (any status, any date).",
     """SELECT order_id, customer_id, restaurant_id, total_amount, status, order_date
FROM orders
ORDER BY total_amount DESC
LIMIT 10;"""),

    ("E4 — Restaurants per city",
     "Number of restaurants in each city, highest first.",
     """SELECT city, COUNT(*) AS n_restaurants
FROM restaurants
GROUP BY city
ORDER BY n_restaurants DESC;"""),

    ("E5 — Cancellations this week",
     "How many orders were cancelled between 2026-04-21 and 2026-04-27?",
     """SELECT COUNT(*) AS cancelled_orders
FROM orders
WHERE status = 'CANCELLED'
  AND order_date BETWEEN '2026-04-21' AND '2026-04-27';"""),

    ("E6 — Restaurants with rating ≥ 4.5 and ≥ 50 reviews",
     "Restaurants with `rating_avg >= 4.5` **and** at least 50 ratings recorded in `ratings`.",
     """SELECT r.restaurant_id, r.name, r.city, r.rating_avg, COUNT(rt.rating_id) AS n_reviews
FROM restaurants r
JOIN orders o    ON r.restaurant_id = o.restaurant_id
JOIN ratings rt  ON o.order_id = rt.order_id
WHERE r.rating_avg >= 4.5
GROUP BY r.restaurant_id, r.name, r.city, r.rating_avg
HAVING COUNT(rt.rating_id) >= 50
ORDER BY r.rating_avg DESC, n_reviews DESC;"""),

    ("E7 — Customers ordering from 5+ different restaurants",
     "Customers who have ordered from at least 5 distinct restaurants.",
     """SELECT c.customer_id, c.name, COUNT(DISTINCT o.restaurant_id) AS n_restaurants
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT o.restaurant_id) >= 5
ORDER BY n_restaurants DESC
LIMIT 20;"""),

    ("E8 — Cities ranked by total revenue this month",
     "Total April delivered revenue per city, highest first.",
     """SELECT r.city, ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'
GROUP BY r.city
ORDER BY revenue DESC;"""),

    ("E9 — Restaurants that have NEVER received an order",
     "LEFT JOIN restaurants to orders; keep where the order side is NULL.",
     """SELECT r.restaurant_id, r.name, r.city
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_id IS NULL
ORDER BY r.name;"""),

    ("E10 — Average order value per cuisine",
     "Average `total_amount` of delivered orders, grouped by cuisine.",
     """SELECT r.cuisine, ROUND(AVG(o.total_amount), 2) AS avg_order_value, COUNT(*) AS n_orders
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.status = 'DELIVERED'
GROUP BY r.cuisine
ORDER BY avg_order_value DESC;"""),

    ("E11 — Top 3 customers by spend in each city (window function)",
     "Per city, the 3 customers with highest total delivered spend.",
     """WITH spend AS (
    SELECT c.city, c.customer_id, c.name,
           SUM(o.total_amount) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'DELIVERED'
    GROUP BY c.city, c.customer_id, c.name
),
ranked AS (
    SELECT city, customer_id, name, total_spend,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_spend DESC) AS rk
    FROM spend
)
SELECT city, name, ROUND(total_spend, 2) AS total_spend
FROM ranked WHERE rk <= 3
ORDER BY city, total_spend DESC;"""),

    ("E12 — Month-over-month revenue growth",
     "Per month, total delivered revenue and the % change vs the previous month.",
     """WITH monthly AS (
    SELECT SUBSTR(order_date, 1, 7) AS month,
           SUM(total_amount)         AS revenue
    FROM orders
    WHERE status = 'DELIVERED'
    GROUP BY SUBSTR(order_date, 1, 7)
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month,
       ROUND( (revenue - LAG(revenue) OVER (ORDER BY month))
              * 100.0
              / LAG(revenue) OVER (ORDER BY month), 2) AS pct_change
FROM monthly
ORDER BY month;"""),

    ("E13 — Most-used promo code this month",
     "Count of orders per promo_code in April. Highest first.",
     """SELECT p.promo_code,
       COUNT(*)                          AS times_used,
       ROUND(SUM(o.total_amount), 2)     AS revenue
FROM orders o
JOIN promotions p ON o.promo_id = p.promo_id
WHERE o.order_date >= '2026-04-01' AND o.status = 'DELIVERED'
GROUP BY p.promo_code
ORDER BY times_used DESC
LIMIT 10;"""),

    ("E14 — Average delivery time per city",
     "From `delivery_assignments`, average minutes between pickup and delivery, grouped by partner's city.",
     """SELECT dp.city,
       ROUND(AVG((JULIANDAY(da.delivery_time) - JULIANDAY(da.pickup_time)) * 1440), 1) AS avg_delivery_min,
       COUNT(*) AS n_completed
FROM delivery_assignments da
JOIN delivery_partners   dp ON da.partner_id = dp.partner_id
WHERE da.delivery_status = 'COMPLETED'
GROUP BY dp.city
ORDER BY avg_delivery_min;"""),

    ("E15 — Top 5 delivery partners by completed deliveries",
     "Partners who completed the most deliveries.",
     """SELECT dp.partner_id, dp.name, dp.city, dp.vehicle,
       COUNT(*) AS completed_deliveries
FROM delivery_assignments da
JOIN delivery_partners   dp ON da.partner_id = dp.partner_id
WHERE da.delivery_status = 'COMPLETED'
GROUP BY dp.partner_id, dp.name, dp.city, dp.vehicle
ORDER BY completed_deliveries DESC
LIMIT 5;"""),
]

# Exercise prompts first (a numbered list)
prompts = "\n".join(f"**{title}** — {desc}\n" for title, desc, _ in EXERCISES)
md(f"""## Try these on your own

{prompts}
> Solutions follow below.
""")

# Then each solution
md("""---
## ✅ Solutions
""")

for title, desc, sol in EXERCISES:
    md(f"### {title}\n\n{desc}\n")
    code(f"""%%sql
{sol}
""")

# ─── Closing ────────────────────────────────────────────────────────────────

md("""---
# 🎬 Closing

You started this hour as a new analyst. Priya asked 9 questions; you wrote 9 SQL queries.
You used aggregates, joins, CTEs, window functions, and case logic — not as buzzwords,
but as natural answers to questions a real business asks.

Take this notebook with you. Re-run the queries. Tweak them. Break them.
The fastest way to get fluent in SQL is to keep asking questions of a table.

**Repo:** [github.com/bcsnpc/quickbite-sql](https://github.com/bcsnpc/quickbite-sql)
""")


# ─── Build notebook JSON ────────────────────────────────────────────────────

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.10",
        },
        "colab": {
            "provenance": [],
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

# Verify it parses
with open(OUT_PATH, "r", encoding="utf-8") as f:
    json.load(f)

print(f"Built {OUT_PATH}")
print(f"  Cells: {len(cells)} ({sum(1 for c in cells if c['cell_type']=='markdown')} md, "
      f"{sum(1 for c in cells if c['cell_type']=='code')} code)")
print(f"  Size:  {os.path.getsize(OUT_PATH):,} bytes")
