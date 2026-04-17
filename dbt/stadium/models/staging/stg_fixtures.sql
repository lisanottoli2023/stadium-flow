{{ config(schema='staging') }}

SELECT
    fixture_id,
    league_id,
    season,
    (raw_json->'fixture'->>'date')::timestamp AS match_date,
    (raw_json->'teams'->'home'->>'id')::integer AS home_team_id,
    (raw_json->'teams'->'away'->>'id')::integer AS away_team_id,
    (raw_json->'goals'->>'home')::integer AS home_goals,
    (raw_json->'goals'->>'away' )::integer AS away_goals,
    raw_json->'fixture'->'status'->>'long' AS status,
    raw_json->'fixture'->'venue'->>'name' AS venue,
    raw_json->'fixture'->>'referee' AS referee

FROM raw.fixtures
