from discord.ext import commands

from discord import app_commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="replies with a ping!")
    async def ping(self, inter):
        await inter.response.send_message("Pong!")


async def setup(bot):
    await bot.add_cog(Utilities(bot))