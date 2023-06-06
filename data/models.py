from dataclasses import dataclass

from functools import cached_property

import typing

import discord
from discord.ui import View

from discord import Embed

BASE_PATH = "./data/assets/characters/"


@dataclass
class Character:
    id: int
    name: str
    description: str
    gender: str
    age: int
    birthday: str
    BD_UNIX: int
    location: str
    image: str
    expressions: list


@dataclass
class Item:
    id: int
    name: str
    character: str | None
    description: str
    world: typing.Union[str, None]
    type: str
    image: str
    hearts: int | None
    juice: int | None
    attack: int | None
    defense: int | None
    speed: int | None
    luck: int | None
    hit_rate: int | None


@dataclass
class Skill:
    id: int
    name: str
    description: str
    type: str
    level: typing.Union[int, str]
    image: str
    juice: int
    character: str

    def __str__(self):
        return self.name


@dataclass
class Enemy:
    id: int
    name: str
    description: str
    world: int
    stage: int
    image: str
    animation: str
    heart: int
    juice: int
    max_heart: int
    attack: int
    defense: int
    speed: int
    luck: int
    hit_rate: int
    skills: list

    def __str__(self):
        return self.name


class Paginator(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user: discord.Member | discord.User | None = None
        self.pages: list[Embed] | None = None
        self.page = 0

    @discord.ui.button(label="<<", style=discord.ButtonStyle.blurple)
    async def absolute_less(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != inter.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return
        if self.page == 0:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        await inter.response.defer()
        self.page = 0
        await inter.message.edit(embed=self.pages[self.page])

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def less(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != inter.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return
        if self.page == 0:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        await inter.response.defer()
        self.page -= 1
        await inter.message.edit(embed=self.pages[self.page])

    @discord.ui.button(label="End Interaction", style=discord.ButtonStyle.red)
    async def end_interaction(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != inter.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return

        await inter.response.defer()

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

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def more(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != inter.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return

        if self.page == len(self.pages) - 1:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        await inter.response.defer()
        self.page += 1
        await inter.message.edit(embed=self.pages[self.page])

    @discord.ui.button(label=">>", style=discord.ButtonStyle.blurple)
    async def absolute_more(self, inter: discord.Interaction, button: discord.Button):
        if self.user.id != inter.user.id:
            await inter.response.send_message("That is not yours?", ephemeral=True)
            return
        if self.page == len(self.pages) - 1:
            await inter.response.send_message("You can't go any further", ephemeral=True)
            return

        await inter.response.defer()
        self.page = len(self.pages) - 1
        await inter.message.edit(embed=self.pages[self.page])


@dataclass
class DataManagerBase:
    # enemies: typing.Dict[int, Enemy] = None
    items: typing.Dict[int, Item] = None
    skills: typing.Dict[int, Skill] = None
    characters: typing.Dict[int, Character] = None
    
    @cached_property
    def list_characters(self):
        return [character.name for character in self.characters.values()]

    @cached_property
    def list_items(self):
        return [item.name for item in self.items.values()]
