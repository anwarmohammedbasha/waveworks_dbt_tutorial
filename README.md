# waveworks_dbt_tutorial

This is a **beginner-friendly dbt project** that demonstrates how to use dbt with DuckDB and a local database file.

Contents
- `README.md` – this file (quick start + commands)
- `models/` – example dbt models (staging + marts)
- `profiles.yml.example` – example dbt profile for DuckDB
- `dbt_project.yml` – dbt project config
- `.gitignore` – recommended ignore file

**Goal:** unzip this project, follow the Quick Start in the README, and run a few `dbt` commands to see transforms.

---

## Quick Start (short)
1. Install Python 3.8+ and pip.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate    # Windows PowerShell
   ```
3. Install dbt and the DuckDB adapter:
   ```bash
   pip install dbt-core dbt-duckdb
   ```
4. Copy the `profiles.yml.example` to your dbt profiles location:
   - Linux/macOS: `~/.dbt/profiles.yml`
   - Windows: `%USERPROFILE%\.dbt\profiles.yml`
5. Place the provided `waveworks.db` file in the same folder you point DuckDB to (see `profiles.yml.example`).
6. From the project root (where this README is), run:
   ```bash
   dbt deps         # if you add packages later
   dbt debug        # checks connection
   dbt run          # build models
   dbt test         # run tests
   dbt docs generate
   dbt docs serve    # view documentation in browser
   ```

---

If a command fails, read the error and adjust `profiles.yml` path to the `waveworks.db` file location.

Good luck — this project is intentionally small so you can read the SQL files and learn how dbt organizes work.

