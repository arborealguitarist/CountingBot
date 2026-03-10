async def process_message(message, db):

    guild_data = await db.get_guild(message.guild.id)

    expected = guild_data["current_count"] + 1
    last_user = guild_data["last_user"]

    try:
        number = int(message.content)
    except:
        return False, "Only integers allowed."

    if number != expected:
        return False, f"Expected {expected}"

    if last_user == message.author.id:
        return False, "You cannot count twice in a row."

    return True, number