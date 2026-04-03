

CREATE SCHEMA IF NOT EXISTS raw;
CREATE TABLE IF NOT EXISTS raw.fixtures (
    fixture_id INTEGER NOT NULL,
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    match_date TIMESTAMPTZ NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    raw_json JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (fixture_id)
);
CREATE TABLE IF NOT EXISTS raw.standings (
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    raw_json JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (league_id, season, team_id)
);
CREATE TABLE IF NOT EXISTS raw.players (
    player_id INTEGER NOT NULL,
    league_id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    raw_json JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (player_id, league_id, season)
);



