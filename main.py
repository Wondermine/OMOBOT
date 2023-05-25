import discord
from discord.ext import commands

import os

from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

import logging

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
        self.E_LIST = ["cogs.utils", "cogs.information"]

    async def on_ready(self):

        for i in self.E_LIST:
            await self.load_extension(i)
            _log.info(f"🔁 | {i} has been loaded")

        await self.tree.sync()
        await self.database_connection()

    async def database_connection(self):
        self.cluster = AsyncIOMotorClient(self.mongo_url)
        self.db = self.cluster["database"]
        self.players = self.db["players"]
        _log.info("✅ | Database connection has been established")


vessel = OMORPG(command_prefix=">", intents=intents, owner_ids=[1051383406598045696])
vessel.run(vessel.token)
