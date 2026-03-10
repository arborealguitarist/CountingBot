import discord
from discord import app_commands

class Commands(app_commands.Group):

    def __init__(self, db):
        super().__init__(name="counting")
        self.db = db

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):

        data = await self.db.leaderboard(interaction.guild.id)

        text = ""
        for i,row in enumerate(data,1):
            user = interaction.guild.get_member(row["user_id"])
            text += f"{i}. {user} — {row['correct_submissions']}\n"

        await interaction.response.send_message(text)

    @app_commands.command()
    async def stats(self, interaction: discord.Interaction):

        stats = await self.db.stats(
            interaction.guild.id,
            interaction.user.id
        )

        await interaction.response.send_message(
            f"""
Highest Number: {stats['highest_number']}
Score: {stats['score']}
Errors: {stats['errors']}
"""
        )

    @app_commands.command()
    async def record(self, interaction: discord.Interaction):

        record = await self.db.server_record(interaction.guild.id)
        await interaction.response.send_message(f"Server record: {record}")

    @app_commands.command()
    async def worldrecord(self, interaction: discord.Interaction):

        record = await self.db.world_record()
        await interaction.response.send_message(f"World record: {record}")