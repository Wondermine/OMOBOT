import enum

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import GroupCog
from discord.app_commands import Choice

from discord.ui import View

import discord

import enum
from typing import Optional, Union

from base import OMOBOT


class Paginator(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.page: int = 1
        self.pages: Union[list, None]
        self.user = Union[discord.User, discord.Member]

    @discord.ui.button(label="<")
    async def less(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != self.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return
        if self.page == 1:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        self.page -= 1
        await inter.response.defer()
        await inter.message.edit(embed=self.pages[self.page - 1])

    @discord.ui.button(label="End Interaction", style=discord.ButtonStyle.red)
    async def end_interaction(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != self.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return

        await inter.response.send_message("Interaction ended", ephemeral=True)

        action = inter.message.components[0]

        buttons = []

        for button in action.children:
            button.disabled = True
            buttons.append(button)

        action.children = buttons

        inter.message.components[0] = action

        view = self.from_message(inter.message)

        await inter.message.edit(view=view)

        self.stop()

    @discord.ui.button(label=">")
    async def more(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != self.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return

        if self.page == 5:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        self.page += 1
        await inter.response.defer()
        await inter.message.edit(embed=self.pages[self.page - 1])


class Characters(enum.Enum):
    OMORI = "OMORI"
    KEL = "KEL"
    AUBREY = "AUBREY"
    HERO = "HERO"
    BASIL = "BASIL"
    MARI = "MARI"


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

        embed = discord.Embed(
            title="OMORI skills"
        )

        if skill is None:
            embed.description = "can't find that skill..."

            embed.set_image(url="https://i.ibb.co/mFK38Tj/notfound.gif")

            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        character = await self.bot.data.find_character_by_name(skill.character)

        embed.description = skill.description

        embed.add_field(name="character", value=skill.character)

        embed.add_field(name="juice", value=f"{skill.juice} <:__:1112092849748594719>")

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
    async def list(self, inter: discord.Interaction, character: Optional[Characters]):

        if character is not None:

            embed = discord.Embed(
                title="OMORI game skills"
            )

            embed.description = f"A list for the skill that {character.value} has"
            character_obj = await self.bot.data.find_character_by_name(character.value)
            embed.set_thumbnail(url=character_obj.image)

            skills = await self.bot.data.find_skills_from_character(character)

            if len(skills) == 0:
                await inter.response.send_message("This character has no skills...", ephemeral=True)
                return

            for skill in skills:
                embed.add_field(name=skill, value=skill.description)

            await inter.response.send_message(embed=embed)
            return

        skills = self.bot.data.skills

        skill_count = 0

        pages = []

        skills_per_page = round(len(skills) / 5)

        embed = discord.Embed(
            title="Game skills",
            description=f"A list of all OMORI skills that exist.\nA total of **{len(skills)}** exist."
        )
        embed.set_footer(text=f"Page 1", icon_url=inter.user.avatar.url)

        view = Paginator(timeout=None)

        for index in skills:
            embed.add_field(name=skills[index].name, value=skills[index].description)

            skill_count += 1

            if skill_count == skills_per_page:
                pages.append(embed)
                skill_count = 0
                embed = discord.Embed(
                    title="Game skills",
                    description=f"A list of all OMORI skills that exist.\nA total of **{len(skills)}** exist."
                )
                embed.set_footer(text=f"Page {len(pages) + 1}", icon_url=inter.user.avatar.url)

        pages.append(embed)

        view.pages = pages
        view.user = inter.user

        await inter.response.send_message("Generating", ephemeral=True)
        await inter.channel.send(embed=pages[0], view=view)


async def setup(bot: OMOBOT):
    await bot.add_cog(SkillCommand(bot))
