from importlib import reload

from discord.ext import commands

import data

from base import OMOBOT


class Data(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

        reload(data)

        self.instance = data.DataManager()


async def setup(bot: OMOBOT):
    await bot.add_cog(Data(bot))
