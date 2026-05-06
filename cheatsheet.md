# QuickBite SQL Cheatsheet

One printable page. Use it as a "what's the shape?" lookup, not a tutorial.

---

## 1. Query skeleton

```sql
SELECT     col1, AGG(col2)        -- what to show
FROM       table_a a
JOIN       table_b b ON a.id = b.a_id
WHERE      col1 = 'value'         -- filter rows BEFORE grouping
GROUP BY   col1
HAVING     AGG(col2) > 100        -- filter groups AFTER aggregation
ORDER BY   AGG(col2) DESC
LIMIT      10;
```

Execution order is **not** the order you write it:
`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

---

## 2. Aggregate functions

| Function | What it returns |
|---|---|
| `COUNT(*)` | Number of rows in the group |
| `COUNT(col)` | Number of non-NULL values in `col` |
| `COUNT(DISTINCT col)` | Number of unique non-NULL values |
| `SUM(col)` | Total of numeric column |
| `AVG(col)` | Mean (NULLs ignored) |
| `MIN(col) / MAX(col)` | Smallest / largest value |

---

## 3. JOIN types

| Join | What you keep |
|---|---|
| `INNER JOIN` | Only rows where the key matches in **both** tables |
| `LEFT JOIN`  | All rows from **left** table; unmatched right side becomes `NULL` |
| `RIGHT JOIN` | All rows from **right** table (rare — usually rewrite as `LEFT JOIN` with sides swapped) |
| `FULL OUTER` | All rows from **both** sides; unmatched → `NULL`. Not in SQLite. |
| `CROSS JOIN` | Every row in A × every row in B (Cartesian) |

Mental model: tables hold hands by an `id` column.

---

## 4. WHERE vs HAVING

| Clause | When it runs | Can it use aggregates? |
|---|---|---|
| `WHERE`  | **Before** grouping — per-row filter | No (`SUM`, `COUNT`, etc. don't exist yet) |
| `HAVING` | **After** grouping — per-group filter | Yes |

```sql
WHERE  status = 'DELIVERED'        -- filter rows
GROUP  BY city
HAVING SUM(total_amount) > 100000  -- filter groups
```

---

## 5. CTEs (Common Table Expressions)

```sql
WITH active AS (
    SELECT customer_id, COUNT(*) AS n
    FROM orders
    WHERE order_date >= '2026-01-01'
    GROUP BY customer_id
),
top_spenders AS (
    SELECT customer_id FROM active WHERE n >= 10
)
SELECT c.name
FROM customers c
JOIN top_spenders t ON c.customer_id = t.customer_id;
```

CTEs are not "advanced" — they're **named steps** that make a query readable.

---

## 6. Window functions

Syntax: `FUNC() OVER (PARTITION BY col1 ORDER BY col2)`

| Function | Behavior |
|---|---|
| `ROW_NUMBER()` | Unique sequence within partition. Ties broken arbitrarily: 1,2,3,4 |
| `RANK()`       | Ties share rank, leaves gaps: 1,2,2,4 |
| `DENSE_RANK()` | Ties share rank, no gaps: 1,2,2,3 |
| `LAG(col)`     | Value from the **previous** row in the partition |
| `LEAD(col)`    | Value from the **next** row in the partition |
| `SUM(col) OVER (...)` | Running total / windowed sum |

`PARTITION BY` ≈ "do it separately for each X but **don't merge** the rows". Unlike `GROUP BY`, the original rows are preserved.

---

## 7. CASE WHEN

```sql
SELECT name,
       CASE
           WHEN rating_avg >= 4.5 THEN '4.5+ stars'
           WHEN rating_avg >= 4.0 THEN '4.0-4.4 stars'
           WHEN rating_avg >= 3.5 THEN '3.5-3.9 stars'
           ELSE 'Below 3.5'
       END AS rating_bucket
FROM restaurants;
```

`CASE` works inside `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY` — anywhere a value is allowed.

---

## 8. Useful patterns

### Top N per group

```sql
WITH ranked AS (
    SELECT city, name, revenue,
           ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rk
    FROM city_revenue
)
SELECT * FROM ranked WHERE rk <= 3;
```

### Find absences (LEFT JOIN + NULL)

```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

### Percentage of total

```sql
SELECT city,
       revenue,
       ROUND(revenue * 100.0 / SUM(revenue) OVER (), 2) AS pct_of_total
FROM city_revenue;
```

### Running total

```sql
SELECT order_date,
       daily_revenue,
       SUM(daily_revenue) OVER (ORDER BY order_date) AS cumulative_revenue
FROM daily;
```

### Gaps and islands (consecutive dates)

```sql
WITH s AS (
    SELECT customer_id, order_date,
           julianday(order_date)
             - ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS streak_id
    FROM (SELECT DISTINCT customer_id, order_date FROM orders)
)
SELECT customer_id, COUNT(*) AS streak_length
FROM s GROUP BY customer_id, streak_id HAVING COUNT(*) >= 5;
```

### List minus list (anti-join)

```sql
SELECT customer_id FROM list_a
WHERE customer_id NOT IN (SELECT customer_id FROM list_b);
-- or, often faster:
SELECT a.customer_id
FROM list_a a
LEFT JOIN list_b b ON a.customer_id = b.customer_id
WHERE b.customer_id IS NULL;
```

---

## 9. SQLite-specific date snippets

| Need | Use |
|---|---|
| Year-month prefix from `'YYYY-MM-DD'` | `SUBSTR(order_date, 1, 7)` |
| Days between dates | `julianday(d2) - julianday(d1)` |
| Minutes between datetimes | `(julianday(t2) - julianday(t1)) * 1440` |
| Today's date | `DATE('now')` |
| 7 days ago | `DATE('now', '-7 days')` |

---

## 10. The five things people forget

1. `COUNT(*)` counts rows; `COUNT(col)` skips `NULL`s.
2. `WHERE col = NULL` doesn't work — use `WHERE col IS NULL`.
3. `GROUP BY` columns must match the non-aggregated `SELECT` columns.
4. `HAVING` happens after `GROUP BY`; `WHERE` happens before.
5. `LIMIT` doesn't undo `ORDER BY` — sort first, trim last.
