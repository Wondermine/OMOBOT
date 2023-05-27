import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

import logging

import traceback

load_dotenv()

intents = discord.Intents.none()

_log = logging.getLogger("discord")


class Colors:
    blue = "\033[94m"
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[1;33m"
    red = "\033[1;31m"
    warn = "\033[93m"
    end = "\033[0m"


class OMORPG(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("TOKEN")
        self.mongo_url = os.getenv("DREAMER")
        self.cluster = None
        self.db = None
        self.players = None

        self.activity = discord.Game("OMORPG | 🔪 under construction")
        self.E_LIST = ["cogs.utils", "cogs.information", "cogs.data", "cogs.game"]

    async def setup_hook(self) -> None:

        # sys.excepthook = self.exception_handler
        for filename in os.listdir("./cogs"):
            if os.path.isfile(os.path.join("./cogs/", filename)):

                try:
                    if filename.endswith(".py"):
                        cog = f"cogs.{filename[:-3]}"
                        _log.info(f"🔁 | {cog} has been loaded")
                        await self.load_extension(cog)

                except Exception as e:
                    print(f"Failed to load cog {filename}")
                    traceback.print_exc()

        await self.tree.sync()
        _log.info(f"✅ | Commands tree has been synced")
        await self.database_connection()

    async def database_connection(self):
        self.cluster = AsyncIOMotorClient(self.mongo_url)
        self.db = self.cluster["database"]
        self.players = self.db["players"]
        _log.info("✅ | Database connection has been established")

    @property
    def data(self):
        return self.get_cog("Data").instance


vessel = OMORPG(command_prefix=">", intents=intents, owner_ids=[1051383406598045696])
vessel.run(vessel.token)
