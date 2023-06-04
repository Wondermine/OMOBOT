import logging
import os
import pathlib
from datetime import datetime
from inspect import getdoc

import discord
import jishaku
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from data import DataManager


class OMOBOT(commands.AutoShardedBot):
    """
    OMOBOT. The OMORI themed discord bot.
    """

    class Embed(discord.Embed):
        def __init__(self, **kwargs):
            color = kwargs.pop("color", 0x2F3136)
            timestamp = kwargs.pop("timestamp", discord.utils.utcnow())
            super().__init__(**kwargs, color=color, timestamp=timestamp)

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            intents=discord.Intents.default(),
            owner_ids=[1051383406598045696],
            strip_after_prefix=True
        )

        self.cluster: AsyncIOMotorClient = AsyncIOMotorClient(os.getenv("DREAMER"))
        self.db: AsyncIOMotorDatabase = self.cluster["database"]
        self.players: AsyncIOMotorDatabase = self.db["players"]

        self.data = DataManager()

        self.activity = discord.Game("OMORI")
        self.status = discord.Status.idle

        self.log = logging.getLogger("discord")

        self.description = getdoc(self)

        self.cog_list = []

        self.help_command = None
        self.launch_time: datetime = datetime.utcnow()

    @property
    def all_extensions(self) -> list[str]:
        exts = pathlib.Path('./bot/ext').glob('**/[!__]*.py')
        exts = ['.'.join(ext.parts).removesuffix('.py') for ext in exts]
        return exts

    @discord.utils.cached_property
    def invite_url(self) -> str:
        return discord.utils.oauth_url(
            client_id=self.user.id,
            permissions=discord.Permissions(40548890369856),
            scopes=["bot", "applications.commands"]
        )

    async def setup_hook(self) -> None:
        return await self.load_all_cogs()

    def get_uptime(self) -> tuple[int, int, int, int]:
        delta = (datetime.utcnow() - self.launch_time)
        delta = round(delta.total_seconds())

        days, left = divmod(delta, 86400)
        hours, left = divmod(left, 3600)
        mins, secs = divmod(left, 60)
        return days, hours, mins, secs

    async def load_all_cogs(self, *, load_jishaku: bool = True) -> None:

        if load_jishaku:
            jishaku.Flags.NO_UNDERSCORE = True
            jishaku.Flags.NO_DM_TRACEBACK = True

            await self.load_extension('jishaku')

        for ext in self.all_extensions:
            try:
                await self.load_extension(ext)
                self.log.info(f'{ext} has been loaded')
            except Exception as e:
                self.log.error(e)

    async def on_connect(self) -> None:
        self.log.info('bot is connected')

    async def on_ready(self) -> None:
        self.log.info('bot is ready')
