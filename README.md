# QuickBite SQL — Learn SQL Through a Story

You're the new data analyst at **QuickBite**, a fictional food delivery startup operating in 8 Indian cities. The CEO walks up to your desk and asks 9 progressively harder questions over the next hour. Each question forces you to learn one new piece of SQL — `SELECT`, `WHERE`, aggregates, `GROUP BY`, joins, CTEs, and window functions. By the end, you've used all of them in real business contexts, not as buzzwords.

## Quick start

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bcsnpc/quickbite-sql/blob/main/notebook/QuickBite_SQL_Story.ipynb)

- **Open in Colab:** click the badge above. Run the setup cell, then work top-to-bottom.
- **View on GitHub:** [`notebook/QuickBite_SQL_Story.ipynb`](notebook/QuickBite_SQL_Story.ipynb)
- **Run locally:** see [`run_locally.md`](run_locally.md) for SQLite/DuckDB/Postgres instructions.

No installation needed for the Colab path. Setup cell takes ~30 seconds.

## What you'll learn

Nine SQL concepts, each tied to a real question Priya asks:

1. **`SELECT … FROM`** — pick columns from a table
2. **`WHERE`** — filter rows
3. **`COUNT / SUM / AVG`** — aggregate functions
4. **`GROUP BY`** — collapse rows that share a value
5. **`ORDER BY` + `LIMIT`** — sort and trim
6. **`INNER JOIN`** — combine two tables on a shared key
7. **`LEFT JOIN`** — keep all rows from one side, even unmatched
8. **CTEs (`WITH`)** — break a query into named, readable steps
9. **Window functions (`OVER PARTITION BY`)** — rank or compare within groups

Bonus: **`CASE WHEN`** for bucketing.

## The dataset

Synthetic data generated reproducibly with `seed=42`. Time period: **2026-01-01 → 2026-04-27** (in the story, "today" is 2026-04-28). All currency in **₹ (Indian Rupees)**.

| Table | Rows | Description |
|---|---|---|
| `customers` | 10,000 | Indian-name customers across 8 cities |
| `restaurants` | 200 | 10 cuisines, weighted toward city-specific cuisines |
| `orders` | ~106K | Customer + restaurant + amount + status + payment |
| `order_items` | ~265K | Per-dish line items |
| `ratings` | ~66K | Star reviews on ~70% of delivered orders |
| `delivery_partners` | 500 | Bike / scooter / bicycle riders |
| `delivery_assignments` | ~98K | Pickup + delivery time + distance |
| `cities` | 8 | Hyderabad, Bangalore, Mumbai, Delhi, Chennai, Pune, Kolkata, Ahmedabad |
| `promotions` | 80 | Promo codes with cuisine and order-value rules |

### Engineered patterns

The customer base is intentionally split into behavior buckets so the teaching queries find clean signal:

- **1,500 regulars** — order 2–3× per week throughout the period
- **1,200 churners** — active in Jan–Feb, **zero** orders in Mar–Apr (the silent-churn query in Act 4 surfaces these)
- **2,000 casual** — order every 2–3 weeks
- **1,500 newcomers** — only ordered Mar–Apr (signed up recently)
- **3,800 sporadic** — 1–3 orders anywhere

Top cuisine per city varies (Hyderabad → Biryani, Bangalore → Continental/Chinese, Pune → Pizza, etc.), so the window-function query in Act 5 produces a genuinely varied result.

## The story (5 acts in 60 minutes)

| Act | Time | Concepts | Priya's question |
|---|---|---|---|
| 🎬 1 — Simple questions | 0:01 – 0:11 | `SELECT`, `WHERE`, `COUNT`, `SUM` | "How did we do yesterday?" |
| 🎬 2 — Grouping | 0:11 – 0:23 | `GROUP BY`, `ORDER BY`, `LIMIT`, first `JOIN` | "Break it down by city. Top 5 restaurants this month?" |
| 🎬 3 — Joins | 0:23 – 0:35 | `INNER JOIN` vs `LEFT JOIN`, find-absence pattern | "Marketing wants names — and a list of customers who've gone silent" |
| 🎬 4 — CTEs | 0:35 – 0:47 | `WITH`, list-minus-list, `HAVING` | "Who are our silent churners?" |
| 🎬 5 — Window functions | 0:47 – 0:55 | `ROW_NUMBER() OVER (PARTITION BY …)` | "What's the top cuisine in each city?" |

The remaining 5 minutes (0:55 – 1:00) is closing recap and Q&A.

Plus a **`CASE WHEN`** bonus for bucketing restaurants by rating.

## Practice on your own

After the notebook, work through 20 progressively harder problems:

- [`exercises/beginner.md`](exercises/beginner.md) — `SELECT`, `WHERE`, aggregates
- [`exercises/intermediate.md`](exercises/intermediate.md) — `GROUP BY`, `HAVING`, joins
- [`exercises/advanced.md`](exercises/advanced.md) — CTEs, window functions, complex date logic
- [`exercises/bonus_promotions_delivery.md`](exercises/bonus_promotions_delivery.md) — uses the `promotions`, `delivery_partners`, `delivery_assignments`, `cities` tables

All solutions: [`solutions/all_solutions.sql`](solutions/all_solutions.sql)

## Run locally without Colab

If you'd rather use DBeaver, DuckDB, or PostgreSQL, see [`run_locally.md`](run_locally.md). The repo includes a one-command `scripts/load_to_sqlite.py` that builds `quickbite.db` from the CSVs.

## Cheatsheet

[`cheatsheet.md`](cheatsheet.md) — one printable page covering query shape, aggregates, join types, the `WHERE`-vs-`HAVING` rule, CTEs, window functions, `CASE WHEN`, and common patterns (top-N-per-group, find-absences, percentage-of-total).

## Regenerating the data

```bash
python scripts/generate_data.py
```

Reproducible with `random.seed(42)` and `numpy.random.seed(42)` — re-running produces identical CSVs.

## Repo layout

```
quickbite-sql/
├── README.md
├── data/                            # 9 CSV files
├── notebook/
│   └── QuickBite_SQL_Story.ipynb    # the main session artifact
├── scripts/
│   ├── generate_data.py             # data generator (seed=42)
│   ├── validate_session_queries.py  # runs all 10 session queries
│   ├── run_all_solutions.py         # runs all 20 exercise solutions
│   ├── build_notebook.py            # rebuilds the .ipynb from source
│   ├── test_notebook_execution.py   # executes notebook end-to-end
│   ├── load_to_sqlite.py            # builds quickbite.db for DBeaver
│   └── schema.sql                   # PostgreSQL DDL for COPY FROM workflow
├── exercises/                       # 4 graded exercise files (20 problems total)
├── solutions/all_solutions.sql      # all 20 solutions, headered & runnable
├── cheatsheet.md                    # one printable page
└── run_locally.md                   # SQLite/DuckDB/Postgres local-run guide
```

## Contributing

PRs welcome — particularly more exercises, bug fixes in queries, or alternate solutions that teach a concept more clearly. Keep the data synthetic; don't add anything that resembles real PII.

## License

MIT. Use it, fork it, run your own session.
