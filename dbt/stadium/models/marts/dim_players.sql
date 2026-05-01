{{ config(schema='marts', materialized='table') }}

SELECT
    player_id,
    league_id,
    season,
    player_name,
    nationality, 
    position, 
    goals,
    assists,
    appearances
FROM {{ ref('stg_players') }}