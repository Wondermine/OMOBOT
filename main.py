import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.none()
class OMORPG(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("TOKEN")

        self.activity = discord.Game("OMORPG | under construstion")
        self.E_LIST = ["cogs.utils", "cogs.information"]

    async def on_shard_connect(self, shard):
        print(f"SHARD {shard} IS UP AND WORKING")
        print(f"currently at {len(self.guilds)} Guilds")
        for i in self.E_LIST:
            await self.load_extension(i)
            print(i)

        await self.tree.sync()


vessel = OMORPG(command_prefix=">", intents=intents, owner_ids=[1051383406598045696])
vessel.run(vessel.token)
