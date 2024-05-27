from discord import Interaction
from discord.app_commands import AppCommandError, CommandOnCooldown
import os
from bot.bot import OMOBOT

from dotenv import load_dotenv
load_dotenv()


def determine_prefix(client, message):
    return [f"<@{client.user.id}>", f"<@!{client.user.id}>"]


if __name__ == "__main__":
    bot = OMOBOT(command_prefix=determine_prefix)

    @bot.tree.error
    async def on_app_command_error(inter: Interaction, error: AppCommandError):
        if isinstance(error, CommandOnCooldown):
            await inter.response.send_message(str(error), ephemeral=True)
            return

        embed = bot.Embed(
            title="An error has occurred",
            description=(
                "```yml\n"
                f"{error}\n"
                "```"
            )
        )
        await inter.followup.send(embed=embed, ephemeral=True)

        raise error

    bot.run(os.getenv("TOKEN"))
