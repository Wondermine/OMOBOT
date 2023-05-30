from discord.ext import commands
import discord
import time

from discord import app_commands

from base import OMOBOT


class Utilities(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Shows the information about the discord latency and how fast the bot can respond!"
    )
    async def ping(self, inter: discord.Interaction):
        """Latency check for stability"""

        await inter.response.send_message("`pinging...`", ephemeral=True)

        msg = await inter.channel.send(f"{inter.user.mention} `pinging...`")

        embed = discord.Embed(
                title="More Information:",
                color=discord.Color.red(),
        )
        start = time.perf_counter()
        await msg.edit(content=f"{inter.user.mention} Trying to ping...")
        end = time.perf_counter()
        speed = round((end - start) * 1000)
        if speed < 160:
            embed.add_field(name=f"Ping:", value=f"🟢 | {speed}ms", inline=True)
        elif speed > 170:
            embed.add_field(name=f"Ping:", value=f"🟡 | {speed}ms", inline=True)
        else:
            embed.add_field(name=f"Ping:", value=f"🔴 | {speed}ms", inline=True)

        embed.set_author(
            name="🏓    PONG    🏓",
            icon_url="https://img.icons8.com/ultraviolet/40/000000/table-tennis.png",
        )
        embed.add_field(
            name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True
        )
        embed.add_field(
            name="Normal Speed",
            value=f"{round(self.bot.latency * 1000) / 4} ms",
        )
        embed.set_footer(text=f"Executed by {inter.user.display_name}", icon_url=inter.user.avatar.url)
        await msg.edit(
            content=f":ping_pong: {inter.user.mention}",
            embed=embed
        )


async def setup(bot: OMOBOT):
    await bot.add_cog(Utilities(bot))
