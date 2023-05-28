from discord.ext.commands.errors import ExtensionError
from motor.motor_asyncio import AsyncIOMotorClient
from discord.ext import commands
from dotenv import load_dotenv
from importlib import reload
from typing import Union
import traceback
import discord
import logging
import data
import os

load_dotenv()

token = os.getenv("TOKEN")


async def determine_prefix(bot, message):
    return [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]


class OMORPG(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.cluster: AsyncIOMotorClient         = None
        # self.data: Union[None, data.DataManager] = None
        # self.db                                  = None
        # self.players                             = None

        self.E_LIST                              = ["cogs.utils", "cogs.information", "cogs.data", "cogs.game"]
        self.activity                            = discord.Game("OMORPG | 🔪 under construction")
        self.log                                 = logging.getLogger("discord")
        # self.mongo_url                           = os.getenv("DREAMER")

    async def setup_hook(self) -> None:
        for filename in os.listdir("./cogs"):
            if os.path.isfile(os.path.join("./cogs/", filename)):

                try:
                    if filename.endswith(".py"):
                        cog = f"cogs.{filename[:-3]}"
                        self.log.info(f"{cog} has been loaded")
                        await self.load_extension(cog)

                except ExtensionError:
                    print(f"Failed to load cog {filename}")
                    traceback.print_exc()

        # await self.tree.sync()
        # self.log.info(f"Commands tree has been synced")

        # await self.database_connection()

        reload(data)
        self.data = data.DataManager()
        await self.load_extension("jishaku")

    async def database_connection(self):
        self.cluster = AsyncIOMotorClient(self.mongo_url)
        self.db = self.cluster["database"]
        self.players = self.db["players"]

        self.log.info("Database connection has been established")


OMORPG(
    command_prefix=determine_prefix,
    intents=discord.Intents.default(),
    owner_ids=[1051383406598045696],
    strip_after_prefix=True
).run(token)
