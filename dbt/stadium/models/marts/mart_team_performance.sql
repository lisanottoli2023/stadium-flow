{{ config(schema='marts', materialized='table') }}

SELECT
    league_id,
    season,
    rank,
    team_name,
    team_id,
    points,
    goals_diff,
    form,
    played,
    wins,
    draws,
    losses,
    goals_for,
    goals_against   
FROM {{ ref('stg_standings') }}