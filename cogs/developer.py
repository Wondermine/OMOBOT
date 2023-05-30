from discord.ext.commands import ExtensionError, ExtensionNotLoaded
import traceback
import discord
import os

from base import OMOBOT
from discord.ext import commands


class DeveloperTools(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx: commands.Context):
        msg = await ctx.send("Reloading...")
        self.bot.cog_list = []

        for filename in os.listdir("./cogs"):
            if os.path.isfile(os.path.join("./cogs/", filename)):
                if filename.endswith(".py"):
                    cog = f"cogs.{filename[:-3]}"
                    try:
                        await self.bot.reload_extension(cog)
                        self.bot.log.info(f"{cog} has been 'reloaded' ")
                        self.bot.cog_list.append(cog)

                    except ExtensionNotLoaded:
                        self.bot.log.info(f"Failed to reload {cog}, trying to load")

                        await self.bot.load_extension(cog)
                        self.bot.cog_list.append(cog)

                        self.bot.log.info(f"{cog} has been reloaded")

                    except ExtensionError:
                        self.bot.log.error(f"Failed to load cog {cog}")

                        traceback.print_exc()

        embed = discord.Embed(
            title="Reloaded",
            description="Reloaded the following cogs"
        )

        for cog_name in self.bot.cogs:

            cog = self.bot.get_cog(cog_name)

            commands_list = []

            raw_commands = cog.get_commands() + cog.get_app_commands()

            count = 0

            if len(raw_commands) > 0:
                for raw_command in raw_commands:
                    count += 1
                    commands_list.append(f"{count}. {raw_command.name}")

            embed.add_field(
                name=cog.__cog_name__,
                value="\n".join(commands_list),
                inline=False
            )

        await msg.edit(content="", embed=embed)


async def setup(bot: OMOBOT):
    await bot.add_cog(DeveloperTools(bot))
