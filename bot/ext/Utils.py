from discord.ext import commands

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

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        print("sync command")
        await self.bot.tree.sync()
        await ctx.send('Command tree synced.')


async def setup(bot: OMOBOT):
    await bot.add_cog(Utilities(bot))
