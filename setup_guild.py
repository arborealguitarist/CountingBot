import discord

CATEGORY_NAME = "BotGames"
CHANNEL_NAME = "countinggame"

async def ensure_guild_setup(guild, db):

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)

    if category is None:
        category = await guild.create_category(CATEGORY_NAME)

    channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

    if channel is None:
        channel = await guild.create_text_channel(
            CHANNEL_NAME,
            category=category
        )

    await db.create_guild(guild.id, channel.id)

    return channel