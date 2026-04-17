
from datetime import datetime, timedelta
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow import DAG
import json 

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def ingest_standings():
   api_key = Variable.get("API_KEY")
   season = Variable.get("season")
   url = "https://v3.football.api-sports.io/standings"
   headers = {"x-apisports-key": api_key}
   params = {"league": 39, "season": season}
   response = requests.get(url, headers=headers, params=params)
   data = response.json()
   standings = data.get("response", [])
   pg_hook = PostgresHook(postgres_conn_id="postgres_default")
   for league in standings:
        league_id = league.get("league", {}).get("id")
        season = league.get("league", {}).get("season")
        for team in league["league"]["standings"][0]:
            team_id = team.get("team", {}).get("id")
            raw_json = json.dumps(team)
            pg_hook.run(
                """
                INSERT INTO raw.standings (league_id, season, team_id, raw_json)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (league_id, season, team_id)
                DO UPDATE SET raw_json = EXCLUDED.raw_json, ingested_at = NOW()
                """,
                parameters=(league_id, season, team_id, raw_json)
            )

def ingest_fixtures():
    api_key = Variable.get("API_KEY")
    season = Variable.get("season")
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": api_key}
    params = {"league": 39, "season": season}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    fixtures = data.get("response", [])
    pg_hook = PostgresHook(postgres_conn_id="postgres_default")
    for fixture in fixtures:
        fixture_id = fixture.get("fixture", {}).get("id")
        league_id = fixture.get("league", {}).get("id")
        season = fixture.get("league", {}).get("season")
        match_date = fixture.get("fixture", {}).get("date")
        home_team_id = fixture.get("teams", {}).get("home", {}).get("id")
        away_team_id = fixture.get("teams", {}).get("away", {}).get("id")
        raw_json = json.dumps(fixture)
        pg_hook.run(
            """
            INSERT INTO raw.fixtures (fixture_id, league_id, season, match_date, home_team_id, away_team_id, raw_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (fixture_id)
            DO UPDATE SET raw_json = EXCLUDED.raw_json, ingested_at = NOW()
            """,
            parameters=(fixture_id, league_id, season, match_date, home_team_id, away_team_id, raw_json)
        )

def ingest_players():
    api_key = Variable.get("API_KEY")
    season = Variable.get("season")
    url = "https://v3.football.api-sports.io/players"
    headers = {"x-apisports-key": api_key}
    params = {"league": 39, "season": season}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    players = data.get("response", [])
    pg_hook = PostgresHook(postgres_conn_id="postgres_default")
    for player in players:
        player_id = player.get("player", {}).get("id")
        league_id = player.get("statistics", [{}])[0].get("league", {}).get("id")
        season = player.get("statistics", [{}])[0].get("league", {}).get("season")
        raw_json = json.dumps(player)
        pg_hook.run(
            """
            INSERT INTO raw.players (player_id, league_id, season, raw_json)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (player_id, league_id, season)
            DO UPDATE SET raw_json = EXCLUDED.raw_json, ingested_at = NOW()
            """,
            parameters=(player_id, league_id, season, raw_json)
        )


with DAG('ingest_football_data', default_args=default_args, schedule_interval='@weekly', catchup=False) as dag:
    ingest_standings_task = PythonOperator(
        task_id='ingest_standings',
        python_callable=ingest_standings
    )
    
    ingest_fixtures_task = PythonOperator(
        task_id='ingest_fixtures',
        python_callable=ingest_fixtures
    )
    
    ingest_players_task = PythonOperator(
        task_id='ingest_players',
        python_callable=ingest_players
    )
