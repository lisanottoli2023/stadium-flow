{{ config(schema='marts', materialized='table') }}

SELECT
    fixture_id,
    league_id,
    season,
    match_date,
    home_team_id,
    away_team_id,
    home_goals,
    away_goals,
    status,
    venue,
    referee
FROM {{ ref('stg_fixtures') }}

