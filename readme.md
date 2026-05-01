# Statdium — End-to-end Football Analytics Pipeline

Ingest match and player data from a public API, orchestrate ingestion with Airflow, model it with dbt (bronze → silver → gold layers), and serve analytics on team performance, player metrics, and match outcomes.

**Pattern:** ELT (Extract → Load → Transform)

![Pipeline Overview](<Screenshot from 2026-03-26 14-10-53.png>)

---

## Stack

| Layer | Tool |
|---|---|
| Orchestration | Apache Airflow 2.8.1 (LocalExecutor) |
| Data Warehouse | PostgreSQL 13 |
| Transformation | dbt-core 1.8 + dbt-postgres |
| Dashboard | Metabase |
| Infrastructure | Docker Compose |
| Language | Python 3.8+ |
| Data Source | API-Football (Premier League) |

---

## Architecture

```
API-Football
     │
     ▼
Airflow DAGs (ingest_football_data)
     │
     ▼
PostgreSQL — raw schema (Bronze)
  ├── raw.fixtures
  ├── raw.standings
  └── raw.players
     │
     ▼
Airflow DAG (trigger_dbt_dag)
     │
     ▼
dbt — staging schema (Silver)
  ├── stg_fixtures
  ├── stg_standings
  └── stg_players
     │
     ▼
dbt — marts schema (Gold)
  ├── fct_match_results
  ├── mart_team_performance
  ├── mart_top_scorers
  └── dim_players
     │
     ▼
Metabase Dashboard
```

---

## DAGs

| DAG | Schedule | Description |
|---|---|---|
| `ingest_football_data` | Weekly | Fetches fixtures, standings, players from API-Football and loads raw JSON into PostgreSQL |
| `trigger_dbt_dag` | Weekly | Runs `dbt run` then `dbt test` after ingestion completes |

Both DAGs include failure alerting via `on_failure_callback`.

---

## dbt Models

**Staging (Silver)** — parse and clean raw JSONB into typed columns

**Marts (Gold)** — analytical models ready for dashboarding
- `fct_match_results` — one row per match with scores, teams, venue
- `mart_team_performance` — standings with wins, draws, losses, goals
- `mart_top_scorers` — player goals + assists leaderboard
- `dim_players` — player profiles with nationality and position

dbt tests (`unique`, `not_null`) on all mart models.

---

## Dashboard (Metabase)

- League standings table
- Team performance bar chart
- Match results table

---

## What I Learned

- Docker Compose and container orchestration
- REST API ingestion with Python
- PostgreSQL schema design with JSONB
- Airflow DAGs with PythonOperator and BashOperator
- dbt medallion architecture (bronze → silver → gold)
- Metabase dashboards

---

## Run Locally

```bash
# Start all services
docker compose up -d

# Initialize raw tables
docker exec -i stadium-flow-postgres-1 psql -U airflow -d statdium_dev < sql/init_raw_tables.sql

# Trigger ingestion in Airflow UI
open http://localhost:8085

# View dashboard
open http://localhost:3000
```
