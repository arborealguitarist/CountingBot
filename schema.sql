CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    current_count INTEGER DEFAULT 0,
    last_user BIGINT,
    record INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS players (
    guild_id BIGINT,
    user_id BIGINT,
    correct_submissions INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    score BIGINT DEFAULT 0,
    highest_number INTEGER DEFAULT 0,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS global_stats (
    id INTEGER PRIMARY KEY DEFAULT 1,
    world_record INTEGER DEFAULT 0
);

INSERT INTO global_stats(id, world_record)
VALUES (1,0)
ON CONFLICT (id) DO NOTHING;