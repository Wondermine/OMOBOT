import discord
import platform
import time

from discord.ext import commands

from discord import app_commands

from bot.bot import OMOBOT


class Information(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @app_commands.checks.cooldown(1, 30.0)
    @app_commands.command(name="info", description="Shows information about OMOBOT.")
    async def information(self, inter: discord.Interaction):
        await inter.response.send_message("working on it", ephemeral=True)

    @app_commands.checks.cooldown(1, 30.0)
    @app_commands.command(name="botinfo", description="Shows information about the instance of the bot")
    async def instance_information(self, inter: discord.Interaction):

        rest_start = time.perf_counter()
        owner = await self.bot.fetch_user(self.bot.owner_ids[0])
        rest_end = time.perf_counter()

        d, h, m, s = self.bot.get_uptime()

        embed = self.bot.Embed(
            title="Project OMOBOT",
            url="https://discord.gg/47vGg2zwPu",
            description=(
                f'[**Invite The Bot**]({self.bot.invite_url})\n'
                f'[**Join our Community**](https://discord.gg/47vGg2zwPu)\n\n'
                "**Description:**\n"
                f'```yml\n'
                f'{self.bot.description}\n'
                f'```\n'
                "**Statistics:**\n"
                '```yml\n'
                f'Developer:  {owner}\n'
                f'Written-in: Python {platform.python_version()}\n'
                f'Library:    {discord.__name__}.py {discord.__version__}\n'
                f'WS-latency: {self.bot.latency * 1000:.1f} ms\n'
                f'REST-latency:  {(rest_end - rest_start) * 1000:.1f} ms\n'
                f'Cog-count:     {len(self.bot.cogs)}\n'
                f'Guild-count: {len(self.bot.guilds)}\n'
                f'User-count:  {sum(g.member_count for g in self.bot.guilds)}\n'
                f'Unique-user-count: {len(set(self.bot.users))}\n\n'
                f'Shard id: {inter.guild.shard_id} / {len(self.bot.shards)}\n'
                f'Uptime:\n  - Days:  {d}\n  - Hours: {h}\n  - Mins:  {m}\n  - Secs:  {s}\n\n'
                '```'
            )
        )
        embed.set_author(
            name=inter.user.display_name,
            icon_url=inter.user.display_avatar.url,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await inter.response.send_message(embed=embed)


async def setup(bot: OMOBOT):
    await bot.add_cog(Information(bot))
