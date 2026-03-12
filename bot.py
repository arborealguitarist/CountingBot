import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from database import Database
from setup_guild import ensure_guild_setup
from game_logic import process_message
from commands import Commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

db = Database()

@bot.event
async def on_ready():

    await db.connect()

    for guild in bot.guilds:
        await ensure_guild_setup(guild, db)

    bot.tree.add_command(Commands(db))
    await bot.tree.sync()

    print(f"Logged in as {bot.user}")


@bot.event
async def on_guild_join(guild):

    await ensure_guild_setup(guild, db)


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    guild_data = await db.get_guild(message.guild.id)

    if guild_data is None:
        return

    if message.channel.id != guild_data["channel_id"]:
        return

    valid, result = await process_message(message, db)

    if not valid:
        
        await db.update_player_error(
            message.guild.id,
            message.author.id
        )

        await db.reset_count(message.guild.id)

        await message.channel.send(
            f"{message.author.mention} broke the count. Restarting at **1**."
        )

        return

    number = result

    await db.update_count(
        message.guild.id,
        number,
        message.author.id
    )

    await db.update_player_success(
        message.guild.id,
        message.author.id,
        number
    )

    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))