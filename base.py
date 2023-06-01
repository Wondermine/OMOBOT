from discord.ext.commands.errors import ExtensionError
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from discord.ext import commands


import traceback
import logging
import discord
from data import DataManager
import os


class OMOBOT(commands.AutoShardedBot):

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            intents=discord.Intents.default(),
            owner_ids=[1051383406598045696],
            strip_after_prefix=True,
            guild_ids=[1101417305897979975],
        )

        self.cluster: AsyncIOMotorClient           = AsyncIOMotorClient(os.getenv("DREAMER"))
        self.db: AsyncIOMotorDatabase              = self.cluster["database"]
        self.players: AsyncIOMotorDatabase         = self.db["players"]

        self.data: data.DataManager                = DataManager()

        self.activity                              = discord.Game("OMOBOT | 🔪 check it out")
        self.log                                   = logging.getLogger("discord")

        self.cog_list                              = []

        self.help_command = None

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        for filename in os.listdir("./cogs"):
            if os.path.isfile(os.path.join("./cogs/", filename)):

                try:
                    if filename.endswith(".py"):
                        cog = f"cogs.{filename[:-3]}"
                        self.log.info(f"{cog} has been loaded")
                        await self.load_extension(cog)
                        self.cog_list.append(cog)

                except ExtensionError:
                    self.log.error(f"Failed to load cog {filename}")
                    traceback.print_exc()
