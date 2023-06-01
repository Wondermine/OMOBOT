import discord
from discord import Interaction
from discord.app_commands import AppCommandError, CommandOnCooldown
import os
from base import OMOBOT


def determine_prefix(bot, message):
    return [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]


if __name__ == "__main__":
    omobot_base = OMOBOT(command_prefix=determine_prefix)

    tree = omobot_base.tree

    @tree.error
    async def on_app_command_error(inter: Interaction, error: AppCommandError):
        if isinstance(error, CommandOnCooldown):
            await inter.response.send_message(str(error), ephemeral=True)
            return

        raise error

    omobot_base.run(os.getenv("TOKEN"))
