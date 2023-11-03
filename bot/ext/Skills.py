from discord import app_commands
from discord.ext.commands import GroupCog
from discord.app_commands import Choice

import discord

from typing import (Optional)

from bot.bot import OMOBOT

from bot.data.models import Paginator

characters_choices = [
            Choice(name="OMORI", value="omori"),
            Choice(name="KEL", value="kel"),
            Choice(name="AUBREY", value="aubrey"),
            Choice(name="BASIL", value="basil"),
            Choice(name="MARI", value="mari")
]


# noinspection PyUnresolvedReferences
class SkillCommand(
    GroupCog,
    name="skills",
    description="Shows you the OMORI game skills from the main characters."
):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @app_commands.command(
        name="find",
        description="Find a skill by name, show information about the skill and where does it come from."
    )
    @app_commands.describe(name="Write a name to find the skill you desire.")
    async def find(self, inter: discord.Interaction, name: str):

        skill = await self.bot.data.find_skill_by_name(name)

        embed = self.bot.Embed(
            title="OMORI skills"
        )

        if skill is None:
            embed.description = "can't find that skill..."

            embed.set_image(url="https://i.ibb.co/mFK38Tj/notfound.gif")

            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        character = await self.bot.data.find_character_by_name(skill.character)

        embed.description = (
            f"🔷 | **Name:** `{skill}`\n"
            f"🔷 | **Character:** `{skill.character}`\n"
            f"🔷 | **Juice:** `{skill.juice}` <:__:1112092849748594719>\n"
            f"🔷 | **Level:** `{skill.level}`\n"
            f"🔷 | **Description:**\n"
            "```yml\n"
            f"{skill.description}\n"
            "```\n"
            "🔷 | **Image:**"
        )

        embed.set_thumbnail(url=character.image)

        if skill.image is None:
            embed.set_image(url="https://i.ibb.co/mFK38Tj/notfound.gif")
        else:
            embed.set_image(url=skill.image)

        await inter.response.send_message(embed=embed)

    @app_commands.command(
        name="list",
        description="List down all skills available, or filter them down by searching for a specific character skills."
    )
    @app_commands.describe(character="Choose a character to display their skills.")
    @app_commands.choices(character=characters_choices)
    async def list(self, inter: discord.Interaction, character: Optional[str]):
        skill_count = 0

        if character is not None:
            embed = self.bot.Embed(
                title="OMORI game skills"
            )

            embed.description = f"A list for the skill that {character} has"
            character_obj = await self.bot.data.find_character_by_name(character)
            embed.set_thumbnail(url=character_obj.image)

            skills = await self.bot.data.find_skills_from_character(character)

            if len(skills) == 0:
                await inter.response.send_message("This character has no skills...", ephemeral=True)
                return

            for skill in skills:
                skill_count += 1
                embed.add_field(
                    name=f"{skill_count}. {skill}",
                    value=(
                        "```yml\n"
                        f"{skill.description}\n"
                        "```"
                    ),
                    inline=False
                )

            embed.set_footer(
                text=f"Skills of the character {character}. {skill_count} Skills in total",
                icon_url=self.bot.user.display_avatar.url
            )

            await inter.response.send_message(embed=embed)
            return

        pages = self.bot.data.skills_pages

        view = Paginator(timeout=200)
        view.user = inter.user
        view.pages = pages

        await inter.response.send_message(embed=view.pages[0], view=view)


async def setup(bot: OMOBOT):
    await bot.add_cog(SkillCommand(bot))
