#!/usr/bin/env python3
"""
check_db.py

Usage:
  - Save this file in your project root (same folder as dbt_project.yml).
  - Activate your project's virtualenv.
  - Run: python check_db.py

What it does:
  - Locates the DuckDB file (looks at ./data/waveworks.duckdb first,
    then reads ~/.dbt/profiles.yml for a duckdb 'path').
  - Connects with duckdb and prints:
      * tables in schema 'main'
      * columns and up to 5 sample rows for:
          - stg_customers
          - stg_orders
          - mart_customers_orders (if present)
"""

from pathlib import Path
import sys

def find_duckdb_path():
    # 1) project data/waveworks.duckdb
    project_path = Path.cwd() / "data" / "waveworks.duckdb"
    if project_path.exists():
        return str(project_path)

    # 2) try to read ~/.dbt/profiles.yml to find a duckdb path
    profiles_file = Path.home() / ".dbt" / "profiles.yml"
    if profiles_file.exists():
        try:
            import yaml
        except Exception:
            # pyyaml may not be installed; try a simple parse fallback
            yaml = None

        try:
            txt = profiles_file.read_text(encoding="utf-8")
            if yaml:
                doc = yaml.safe_load(txt)
            else:
                # very small fallback: search for 'path:' line under duckdb
                doc = None

            # If we have a parsed doc, search for first duckdb path
            if isinstance(doc, dict):
                for prof_name, prof_conf in doc.items():
                    outputs = prof_conf.get("outputs", {}) if isinstance(prof_conf, dict) else {}
                    target = prof_conf.get("target") if isinstance(prof_conf, dict) else None
                    # pick target output first
                    if target and target in outputs:
                        out = outputs[target]
                        if out.get("type") == "duckdb" and out.get("path"):
                            return str(Path(out["path"]))
                    # fallback: search all outputs
                    for out in outputs.values():
                        if isinstance(out, dict) and out.get("type") == "duckdb" and out.get("path"):
                            return str(Path(out["path"]))
            else:
                # naive text search fallback
                for line in txt.splitlines():
                    l = line.strip()
                    if l.startswith("path:"):
                        candidate = l.split(":", 1)[1].strip().strip('"').strip("'")
                        if candidate.endswith(".duckdb"):
                            return candidate
        except Exception:
            pass

    return None

def show_table_info(con, schema, table):
    try:
        cols = [r[0] for r in con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema=? AND table_name=?",
            [schema, table]
        ).fetchall()]
    except Exception as e:
        print(f"  [could not read columns for {schema}.{table}] {e}")
        return

    print(f"\nColumns for {schema}.{table}:")
    print("  ", cols)

    try:
        rows = con.execute(f"SELECT * FROM {schema}.{table} LIMIT 5").fetchall()
        print(f"\nSample rows from {schema}.{table} (up to 5):")
        for r in rows:
            print("  ", r)
    except Exception as e:
        print(f"  [could not read sample rows for {schema}.{table}] {e}")

def main():
    duck_path = find_duckdb_path()
    if not duck_path:
        print("ERROR: Could not find a DuckDB file automatically.")
        print("Try placing your duckdb file at ./data/waveworks.duckdb or check ~/.dbt/profiles.yml")
        sys.exit(1)

    print("Using DuckDB file:", duck_path)
    try:
        import duckdb
    except Exception as e:
        print("ERROR: duckdb Python package not found. Install it in your venv: pip install duckdb")
        sys.exit(1)

    try:
        con = duckdb.connect(duck_path)
    except Exception as e:
        print("ERROR: Could not open DuckDB file:", e)
        sys.exit(1)

    try:
        tables = [r[0] for r in con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='main'"
        ).fetchall()]
        print("\nTables in schema 'main':")
        for t in tables:
            print("  -", t)
    except Exception as e:
        print("ERROR: Could not list tables:", e)
        con.close()
        sys.exit(1)

    # check a few important models
    for t in ("stg_customers", "stg_orders", "mart_customers_orders"):
        if t in tables:
            show_table_info(con, "main", t)
        else:
            print(f"\nNote: table {t} not found in main schema.")

    con.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
