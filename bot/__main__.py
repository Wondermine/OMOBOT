from discord import Interaction
from discord.app_commands import AppCommandError, CommandOnCooldown
import os
from .bot import OMOBOT


def determine_prefix(bot, message):
    return [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]


if __name__ == "__main__":
    bot = OMOBOT(command_prefix=determine_prefix)

    tree = bot.tree

    @tree.error
    async def on_app_command_error(inter: Interaction, error: AppCommandError):
        if isinstance(error, CommandOnCooldown):
            await inter.response.send_message(str(error), ephemeral=True)
            return

        embed = bot.Embed(
            title="An error has occured",
            description=(
                "```yml\n"
                f"{error}\n"
                "```"
            )
        )
        await inter.followup.send(embed=embed, ephemeral=True)

        raise error

    bot.run(os.getenv("TOKEN"))
