from discord import app_commands
from discord.ext import commands
import discord
import time

class GameCommands(commands.Cog):
    def __init__(self, bot:commands.AutoShardedBot):
        self.bot = bot

    @app_commands.command(name="skills", description="Show you details about OMORI skills ingame")
    async def skills(self, inter:discord.Interaction):
        embed=discord.Embed(
            title="OMORI Skills",
            color=discord.Color.red()
        )

        for index in self.bot.data.skills:
            skill = self.bot.data.skills[index]
            embed.add_field(
                name=f"{index + 1}. {skill.name}",
                value=f"Description: **{skill.description}**")

        await inter.response.send_message(embed=embed)

async def setup(bot: commands.AutoShardedBot):
    await bot.add_cog(GameCommands(bot))