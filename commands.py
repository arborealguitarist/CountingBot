import discord
from discord import app_commands

class Commands(app_commands.Group):

    def __init__(self, db):
        super().__init__(name="counting")
        self.db = db

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        data = await self.db.leaderboard(interaction.guild.id)

        if not data:
            await interaction.response.send_message("No leaderboard data yet.")
            return

        lines = []

        for i, row in enumerate(data, 1):
            user_id = row["user_id"]

            member = interaction.guild.get_member(user_id)
            if member is None:
                try:
                    member = await interaction.guild.fetch_member(user_id)
                except discord.NotFound:
                    member = None
                except discord.Forbidden:
                    member = None
                except discord.HTTPException:
                    member = None

            name = member.display_name if member else f"User {user_id}"
            lines.append(f"{i}. {name} — {row['correct_submissions']}")

        await interaction.response.send_message("\n".join(lines))

    @app_commands.command()
    async def stats(self, interaction: discord.Interaction):

        stats = await self.db.stats(
            interaction.guild.id,
            interaction.user.id
        )

        await interaction.response.send_message(
            f"""
    Correct Submissions: {stats['correct_submissions']}
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