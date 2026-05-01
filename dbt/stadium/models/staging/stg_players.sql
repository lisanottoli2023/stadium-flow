{{ config(schema='staging') }}

SELECT
    player_id,
    league_id,
    season,
    raw_json->'player'->>'name' AS player_name,
    raw_json->'player'->>'nationality' AS nationality,
    raw_json->'statistics'->0->>'position' AS position,
    (raw_json->'statistics'->0->'goals'->>'total')::integer AS goals,
    (raw_json->'statistics'->0->'goals'->>'assists')::integer AS assists,
    (raw_json->'statistics'->0->'games'->>'appearences')::integer AS appearances

FROM raw.players