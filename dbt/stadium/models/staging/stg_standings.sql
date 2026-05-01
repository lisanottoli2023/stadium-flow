
{{ config(schema='staging') }}

SELECT
    league_id,
    season,
    (raw_json->>'rank')::integer                    AS rank,
    raw_json->'team'->>'name'                       AS team_name,
    (raw_json->'team'->>'id')::integer              AS team_id,
    (raw_json->>'points')::integer                  AS points,
    (raw_json->>'goalsDiff')::integer           AS goals_diff,
    raw_json->> 'form'                              AS form,
    (raw_json->'all'->>'played')::integer          AS played,
    (raw_json->'all'->>'win')::integer             AS wins,
    (raw_json->'all'->>'draw')::integer            AS draws,
    (raw_json->'all'->>'lose')::integer            AS losses,
    (raw_json->'all'->'goals'->>'for')::integer    AS goals_for,
    (raw_json->'all'->'goals'->>'against')::integer AS goals_against






    
FROM raw.standings
