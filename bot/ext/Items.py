from discord import app_commands
from discord.ext.commands import GroupCog
from discord.app_commands import Choice

import discord

from typing import (Optional, Union, Iterable)

from bot.bot import OMOBOT

from data.models import Paginator

characters_choices = [
            Choice(name="OMORI", value="omori"),
            Choice(name="KEL", value="kel"),
            Choice(name="AUBREY", value="aubrey"),
            Choice(name="BASIL", value="basil"),
            Choice(name="MARI", value="mari"),
            Choice(name="SUNNY", value="sunny")
]

item_choices = [
            Choice(name="Weapons", value="weapon"),
            Choice(name="Charms", value="charm"),
            Choice(name="Snacks", value="snack"),
            Choice(name="Toys", value="toy"),
            Choice(name="important_item", value="important item")
]


class ItemsCommand(
    GroupCog,
    name="items",
    description="Shows you the OMORI game items from the main characters."
):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @app_commands.rename(kind="type")
    @app_commands.choices(character=characters_choices, kind=item_choices)
    @app_commands.command(name="list", description="List all the items of OMORI game")
    async def list(
            self,
            inter: discord.Interaction,
            character: Optional[str],
            kind: Optional[str]
    ):
        items_count = 0

        if kind is not None and character is not None:
            await inter.response.send_message(
                "You cannot use both arguments, use either `type` or `character`",
                ephemeral=True
            )
            return

        if character is not None:
            embed = self.bot.Embed(
                title="OMORI game items"
            )
            embed.description = f"A list for the items that {character} has"
            character_obj = await self.bot.data.find_character_by_name(character)
            embed.set_thumbnail(url=character_obj.image)

            items = await self.bot.data.find_items_from_character(character)

            if len(items) == 0:
                await inter.response.send_message("This character has no items...", ephemeral=True)
                return

            for item in items:
                items_count += 1
                embed.add_field(
                    name=f"{items_count}. {item.name}",
                    value=(
                        "```yml\n"
                        f"{item.description}\n"
                        "```"
                    ),
                    inline=False
                )

            embed.set_footer(
                text=f"Items of the character {character}. {items_count} Items in total",
                icon_url=self.bot.user.display_avatar.url
            )

            await inter.response.send_message(embed=embed)
            return

        if kind is not None:
            if kind == "important":
                kind = "important item"

            pages = self.bot.data.kind_pages[kind]

            view = Paginator(timeout=200)
            view.user = inter.user
            view.pages = pages

            await inter.response.send_message(embed=pages[0], view=view)
            return

        view = Paginator(timeout=200)

        pages = self.bot.data.items_pages["item"]
        view.user = inter.user
        view.pages = pages

        await inter.response.send_message(embed=pages[0], view=view)

    @app_commands.command(name="find", description="Find an item based on your query.")
    async def find(self, inter: discord.Interaction, name: str):

        item = await self.bot.data.find_item_by_name(name)

        embed = self.bot.Embed(
            title="OMORI Items"
        )

        if item is None:
            embed.description = f"can't find {name}..."

            embed.set_image(url="https://i.ibb.co/mFK38Tj/notfound.gif")

            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        if item.type == "weapon":
            embed.description = (
                f"🔷 | **Name:** `{item.name}`\n"
                
                f"🔷 | **Character:** `{item.character}`\n"
                
                f"🔷 | **World:** `{item.world}`\n"
                
                f"🔷 | **Hearts:** `{item.hearts}` <:__:1115552945438728192>\n"
                
                f"🔷 | **Juice:** `{item.juice}` <:__:1112092849748594719>\n"
                
                f"🔷 | **Attack:** `{item.attack}`\n"
                
                f"🔷 | **Defense:** `{item.defense}`\n"
                
                f"🔷 | **Speed:** `{item.speed}`\n"
                
                f"🔷 | **Luck:** `{item.luck}`\n"
                
                f"🔷 | **Hit Rate:** `{item.hit_rate}`\n"
                
                f"🔷 | **Description:**\n"
                "```yml\n"
                f"{item.description}\n"
                "```\n"
                
                "🔷 | **Image:**"
                )
            character = await self.bot.data.find_character_by_name(item.character)
            embed.set_thumbnail(url=character.image)
            embed.set_image(url=item.image)

        elif item.type in ["charm", "toy"]:
            embed.description = (
                f"🔷 | **Name:** `{item.name}`\n"

                f"🔷 | **World:** `{item.world}`\n"
                
                f"🔷 | **Hearts:** `{item.hearts}` <:__:1115552945438728192>\n"
                
                f"🔷 | **Juice:** `{item.juice}` <:__:1112092849748594719>\n"
                
                f"🔷 | **Attack:** `{item.attack}`\n"
                
                f"🔷 | **Defense:** `{item.defense}`\n"
                
                f"🔷 | **Speed:** `{item.speed}`\n"
                
                f"🔷 | **Luck:** `{item.luck}`\n"
                
                f"🔷 | **Hit Rate:** `{item.hit_rate}`\n"

                f"🔷 | **Description:**\n"
                "```yml\n"
                f"{item.description}\n"
                "```\n"
            )
            embed.set_thumbnail(url=item.image)

        elif item.type == "snack":
            embed.description = (
                f"🔷 | **Name:** `{item.name}`\n"

                f"🔷 | **World:** `{item.world}`\n"

                f"🔷 | **Hearts:** `{item.hearts}` <:__:1115552945438728192>\n"

                f"🔷 | **Juice:** `{item.juice}` <:__:1112092849748594719>\n"

                f"🔷 | **Description:**\n"
                "```yml\n"
                f"{item.description}\n"
                "```\n"
            )
            embed.set_thumbnail(url=item.image)

        elif item.type == "important item":
            embed.description = (
                f"🔷 | **Name:** `{item.name}`\n"

                f"🔷 | **World:** `{item.world}`\n"

                f"🔷 | **Description:**\n"
                "```yml\n"
                f"{item.description}\n"
                "```\n"
            )
            embed.set_thumbnail(url=item.image)
        else:
            print("IMPOSSIBLE!")

        await inter.response.send_message(embed=embed)


async def setup(bot: OMOBOT):
    await bot.add_cog(ItemsCommand(bot))
