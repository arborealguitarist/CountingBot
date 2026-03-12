import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):
        self.pool = None

    async def connect(self):
    #    self.pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
        self.pool = await asyncpg.create_pool(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            host=os.environ["DB_HOST"],
        )

    async def get_guild(self, guild_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM guilds WHERE guild_id=$1",
                guild_id
            )

    async def create_guild(self, guild_id, channel_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO guilds(guild_id, channel_id)
                VALUES($1,$2)
                ON CONFLICT (guild_id) DO NOTHING
                """,
                guild_id, channel_id
            )

    async def update_count(self, guild_id, count, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE guilds
                SET current_count=$1, last_user=$2,
                record = GREATEST(record,$1)
                WHERE guild_id=$3
                """,
                count, user_id, guild_id
            )

    async def reset_count(self, guild_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE guilds
                SET current_count=0, last_user=NULL
                WHERE guild_id=$1
                """,
                guild_id
            )

    async def update_player_success(self, guild_id, user_id, number):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO players (
                    guild_id,
                    user_id,
                    correct_submissions,
                    errors,
                    score,
                    highest_number
                )
                VALUES ($1, $2, 1, 0, $3, $3)
                ON CONFLICT (guild_id, user_id)
                DO UPDATE SET
                    correct_submissions = players.correct_submissions + 1,
                    score = players.score + $3,
                    highest_number = GREATEST(players.highest_number, $3)
                """,
                guild_id,
                user_id,
                number
            )

    async def update_player_error(self, guild_id, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO players(guild_id,user_id,errors)
                VALUES($1,$2,1)
                ON CONFLICT (guild_id,user_id)
                DO UPDATE SET errors = players.errors + 1
                """,
                guild_id, user_id
            )

    async def leaderboard(self, guild_id):
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT user_id, correct_submissions
                FROM players
                WHERE guild_id=$1
                ORDER BY correct_submissions DESC
                LIMIT 3
                """,
                guild_id
            )

    async def stats(self, guild_id, user_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                """
                SELECT correct_submissions, highest_number, score, errors
                FROM players
                WHERE guild_id=$1 AND user_id=$2
                """,
                guild_id, user_id
            )

    async def server_record(self, guild_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT record FROM guilds WHERE guild_id=$1",
                guild_id
            )

    async def world_record(self):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT MAX(record) FROM guilds"
            )