# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This workspace contains Python scripts for querying Azure Synapse Analytics and auto-generating HTML dashboards from the results. There is also a `calculator/` project (static HTML) and a `todo-next/` Next.js project.

## Running the Pipeline

The main workflow is a 3-step pipeline orchestrated by `Totalagent.py`:

```bash
python Totalagent.py
```

This runs sequentially:
1. **Step 1** — Verifies Azure Synapse connection using credentials from `InfoU.ini`
2. **Step 2** — Prompts for a SQL query (multiline, blank line to submit), exports result to `YYYYMMDDHHMMSS.csv`
3. **Step 3** — Finds the latest timestamped CSV, generates `dashboard_YYYYMMDDHHMMSS.html`, and opens it in the browser

Each step can also be run independently:

```bash
python PBconnect.py                        # Step 1: connection test only
echo "SELECT TOP 10 * FROM table" | python 2ndStep.py   # Step 2: query → CSV
python dashboard_agent.py                  # Step 3: latest CSV → dashboard
```

## Credentials

`InfoU.ini` stores Azure AD credentials on the first line as `username/password`. This file must exist in `D:\claude\` before running any script. It is read by `PBconnect.py`, `2ndStep.py`, and inlined into `Totalagent.py`.

- **Server**: `synapse-workspace-si.sql.azuresynapse.net`
- **Database**: `sibidb`
- **Auth**: `ActiveDirectoryPassword` via ODBC Driver 18 for SQL Server

## Dashboard Auto-Generation (`dashboard_agent.py`)

The dashboard agent detects column types and builds charts based on well-known column name conventions in the `sibidb` schema:

| Column | Chart |
|---|---|
| `ORNZ_NM_3` | Bar chart by team/org unit |
| `STOR_CD` / `STOR_NM` | Bar chart by store (top 10) |
| `DSBT_LGRP_CD` / `DSBT_LGRP_NM` | Bar chart by distribution subgroup (top 10) |
| `BRAN_CD` / `BRAN_NM` | Bar chart by brand |

If none of these columns exist, it falls back to auto-detecting categorical columns (≤30 unique values). The first non-code numeric column (skipping suffixes: `CD`, `NM`, `DT`, `YN`, `NO`, `ID`, `SEQ`) is used as the metric.

## Custom Slash Command

`/QuerybaseAgent` — runs `Totalagent.py` and handles the interactive SQL input in step 2. Use this command when the user wants to query the database and generate a dashboard.

## Dependencies

Required Python packages: `pyodbc`, `pandas`, `plotly`

System requirement: **ODBC Driver 18 for SQL Server** must be installed.
