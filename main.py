import os
from base import OMOBOT


def determine_prefix(bot, message):
    return [f"<@{bot.user.id}>", f"<@!{bot.user.id}>"]


if __name__ == "__main__":
    OMOBOT(command_prefix=determine_prefix).run(os.getenv("TOKEN"))
