from importlib import reload

from discord.ext import commands

import data

class Data(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

        reload(data)

        self.instance = data.DataManager()

async def setup(bot:commands.AutoShardedBot):
    await bot.add_cog(Data(bot))