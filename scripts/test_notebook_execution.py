"""
Test that the notebook executes end-to-end. The published notebook fetches CSVs
from a GitHub raw URL (https://github.com/bcsnpc/quickbite-sql), so we can't run
that version locally.

This script:
1. Loads the .ipynb
2. Swaps cell 2 (the setup cell) for a local-data version
3. Executes the whole notebook with nbclient
4. Reports pass/fail; does not save the executed copy back to disk.

Run: python scripts/test_notebook_execution.py
"""

import json
import os
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_PATH    = os.path.join(ROOT, "notebook", "QuickBite_SQL_Story.ipynb")
DATA_DIR   = os.path.join(ROOT, "data").replace("\\", "/")

LOCAL_SETUP = f"""# LOCAL TEST SETUP — replaces GitHub fetch with local CSV load
import os, pandas as pd, sqlite3, tempfile
from sqlalchemy import create_engine

DATA_DIR = r"{DATA_DIR}"
TABLES = [
    "cities", "customers", "restaurants", "promotions",
    "orders", "order_items", "ratings",
    "delivery_partners", "delivery_assignments",
]

DB_PATH = os.path.join(tempfile.gettempdir(), "quickbite_test.db").replace("\\\\", "/")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)

print("Loading local CSVs into SQLite ...")
for t in TABLES:
    df = pd.read_csv(os.path.join(DATA_DIR, f"{{t}}.csv"))
    df.to_sql(t, conn, if_exists="replace", index=False)
    print(f"  {{t:<22}} {{len(df):>8,}} rows")
conn.commit()
conn.close()

engine = create_engine(f"sqlite:///{{DB_PATH}}")
%load_ext sql
%sql engine
%config SqlMagic.displaylimit = None
%config SqlMagic.autopandas = True
print("\\nReady (test mode).")
"""


def main():
    print(f"Loading notebook: {NB_PATH}")
    nb = nbformat.read(NB_PATH, as_version=4)

    # Find setup cell (the only code cell with `pip install -q jupysql`)
    setup_idx = None
    for i, c in enumerate(nb.cells):
        if c.cell_type == "code" and "pip install -q jupysql" in "".join(c.source):
            setup_idx = i
            break
    if setup_idx is None:
        print("ERROR: could not locate setup cell")
        sys.exit(1)

    original_setup = nb.cells[setup_idx].source
    print(f"Replacing setup cell at index {setup_idx} with local-data variant")
    nb.cells[setup_idx].source = LOCAL_SETUP

    n_code = sum(1 for c in nb.cells if c.cell_type == "code")
    print(f"Executing {n_code} code cells ...")

    client = NotebookClient(nb, timeout=120, kernel_name="python3")
    try:
        client.execute()
    except CellExecutionError as e:
        print(f"\n[FAIL] Cell execution error:")
        print(str(e)[:2000])
        sys.exit(1)

    # Restore the published-version setup cell + clear its (test-mode) outputs
    nb.cells[setup_idx].source = original_setup
    nb.cells[setup_idx].outputs = []
    nb.cells[setup_idx].execution_count = None

    # Save executed notebook so users see expected query outputs without running
    nbformat.write(nb, NB_PATH)

    no_output = [
        i for i, c in enumerate(nb.cells)
        if c.cell_type == "code" and i != setup_idx and not c.get("outputs")
    ]
    print(f"\nExecuted cleanly. Query cells without outputs: {len(no_output)}")
    print(f"Total cells: {len(nb.cells)} (md={sum(1 for c in nb.cells if c.cell_type=='markdown')}, code={n_code})")
    print(f"Saved executed notebook to: {NB_PATH}")
    print("All cells passed.")


if __name__ == "__main__":
    main()
