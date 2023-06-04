from discord.ext import commands
import discord
import time

from discord import app_commands

from bot.bot import OMOBOT


class Utilities(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        for cog in self.bot.all_extensions:
            await self.bot.reload_extension(cog)

        await ctx.reply("reloaded all stuff?")


async def setup(bot: OMOBOT):
    await bot.add_cog(Utilities(bot))
