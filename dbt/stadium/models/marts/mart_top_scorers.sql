{{ config(schema='marts', materialized='table') }}


SELECT
    player_id,
    player_name,
    nationality,
    position,
    goals,
    season,
    assists,
    appearances,
    COALESCE(goals, 0) + COALESCE(assists, 0) AS goal_contributions
FROM {{ ref('stg_players') }}
ORDER BY goal_contributions DESC
