from . import models

import csv

import json
import discord
import asyncio

from pathlib import Path

class Embed(discord.Embed):
    def __init__(self, **kwargs):
        color = kwargs.pop("color", 0x2F3136)
        timestamp = kwargs.pop("timestamp", discord.utils.utcnow())
        super().__init__(**kwargs, color=color, timestamp=timestamp)


def isnumber(v):
    try:
        int(v)
    except ValueError:
        return False
    return True


def get_data_from(filename):
    path = Path(__file__).parent / "csv" / filename

    with open(path) as f:
        reader = csv.DictReader(f)
        raw_data = list(
            {k: int(v) if isnumber(v) else v for k, v in row.items() if v != ""}
            for row in reader
        )

    return raw_data


def get_data_from_json(filename):
    path = Path(__file__).parent / "data" / filename

    with open(path) as f:
        raw_data = json.loads(f.read())

        return raw_data


def get_items():
    items_data = get_data_from_json("items.json")

    items = {}

    for idx in items_data:
        item = items_data[idx]

        items[item["id"]] = models.Item(
            id=item["id"],
            name=item["name"],
            character=item["character"],
            description=item["description"],
            world=item["world"],
            type=item["type"],
            image=item["image"],
            hearts=item["hearts"],
            juice=item["juice"],
            attack=item["attack"],
            defense=item["defense"],
            speed=item["speed"],
            luck=item["luck"],
            hit_rate=item["hit_rate"]
        )

    return items


def get_skills():
    data = get_data_from_json("skills.json")

    skills = {}

    for skill_name in data["DreamWorld"]:
        skill_obj = data["DreamWorld"][skill_name]

        skills[skill_name] = models.Skill(
            id=skill_obj["id"],
            name=skill_obj["name"],
            description=skill_obj["description"],
            type=skill_obj["type"],
            level=skill_obj["level"],
            juice=skill_obj["juice"],
            image=skill_obj["image"],
            character=skill_obj["character"]
        )

    return skills


def get_enemies():
    enemies_data = get_data_from("enemies.csv")

    enemies = {}

    for row in enemies_data:
        enemies[row["id"]] = models.Enemy(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            world=row["world"],
            stage=row["stage"],
            image=row["image"],
            animation=row["animation"],
            heart=row["heart"],
            max_heart=row["max_heart"],
            attack=row["attack"],
            defense=row["defense"],
            speed=row["speed"],
            juice=row["juice"],
            luck=row["luck"],
            hit_rate=row["hit_rate"],
            skills=row["skills"]
        )
    return enemies


def get_characters():
    data = get_data_from_json("characters.json")

    characters = {}

    for character_name in data:

        character = data[character_name]

        characters[character["id"]] = models.Character(
            id=character["id"],
            name=character["name"],
            description=character["description"],
            gender=character["gender"],
            age=character["age"],
            birthday=character["birthday"],
            BD_UNIX=character["BD_UNIX"],
            location=character["location"],
            expressions=character["expressions"],
            image=character["image"]
        )

    return characters


async def generate_items_embed(instance, list_of_types: bool = False):
    if list_of_types:
        types = {
            "weapon": [],
            "charm": [],
            "toy": [],
            "snack": [],
            "important item": []
        }
        pages = {
            "weapon": [],
            "charm": [],
            "toy": [],
            "snack": [],
            "important item": []
        }

        for kind in types:
            types[kind] = await instance.find_items_by_type(kind)
    else:
        types = {"item": instance.items}
        pages = {"item": []}

    for kind in types:
        total_items = 0
        items_count = 0
        pages_count = 1

        items_per_page = 11

        embed = Embed(
            title=f"Game {kind.capitalize()}s",
            description=(
                f"A list of `OMORI` **{kind.capitalize()}s**.\n"
                f"A total of **{len(types[kind]) - 1}** {kind}s exist."
            )
        )

        embed.set_footer(text=f"Page {pages_count}")

        for index in types[kind]:
            if isinstance(index, type(instance.items[0])):
                item = index
            else:
                item = types[kind][index]

            items_count += 1
            embed.add_field(
                name=f"{total_items}. {item.name}",
                value=(
                    "```yml\n"
                    f"{item.description}\n"
                    "```"
                ),
                inline=False
            )

            total_items += 1

            if items_count == items_per_page:
                pages_count += 1
                pages[kind].append(embed)
                items_count = 0
                embed = Embed(
                    title=f"Game {kind.capitalize()}s",
                    description=(
                        f"A list of `OMORI` **{kind.capitalize()}s**.\n"
                        f"A total of **{len(types[kind]) - 1}** {kind}s exist."
                    )
                )
                embed.set_footer(text=f"Page {pages_count}")

        pages[kind].append(embed)

    return pages


async def generate_skills_embed(instance):
    skills = instance.skills

    skill_count = 0
    pages_count = 1

    total_skills = 0

    pages = []

    skills_per_page = 11

    embed = Embed(
        title="Game skills",
        description=f"A list of all OMORI skills that exist.\nA total of **{len(skills)}** Skills exist."
    )
    embed.set_footer(text=f"Page {pages_count}")

    for index in skills:
        total_skills += 1
        embed.add_field(
            name=f"{total_skills}. {skills[index].name}",
            value=(
                "```yml\n"
                f"{skills[index].description}\n"
                "```"
            ),
            inline=False
        )

        skill_count += 1

        if skill_count == skills_per_page:
            pages_count += 1
            pages.append(embed)
            skill_count = 0
            embed = Embed(
                title="Game skills",
                description=f"A list of all `OMORI` skills that exist.\nA total of **{len(skills)}** exist."
            )
            embed.set_footer(text=f"Page {pages_count}")

    pages.append(embed)

    return pages


class DataManager(models.DataManagerBase):
    def __init__(self):
        self.items = get_items()
        self.skills = get_skills()
        # self.enemies = get_enemies()
        self.characters = get_characters()

        self.items_pages = asyncio.run(generate_items_embed(self))
        self.skills_pages = asyncio.run(generate_skills_embed(self))

        self.kind_pages = asyncio.run(generate_items_embed(self, True))

    async def find_character_by_name(self, name: str) -> Character | None:
        for index in self.characters:
            character = self.characters[index]
            if character.name.lower() == name.lower():
                return character
        return None

    async def find_skill_by_name(self, name: str):
        for index in self.skills:
            skill = self.skills[index]
            if skill.name.lower() == name.lower():
                return skill
        return None

    async def find_item_by_name(self, name: str):
        for idx in self.items:
            item = self.items[idx]
            if name.lower() == item.name.lower():
                return item
        return None

    async def find_items_by_type(self, kind: str):
        items = []
        for idx in self.items:
            item = self.items[idx]
            if kind.lower() == item.type.lower():
                items.append(item)

        return items

    async def find_skills_from_character(self, character: str):
        skills = []
        for index in self.skills:
            skill = self.skills[index]
            if skill.character.lower() == character.lower():
                skills.append(skill)

        return skills

    async def find_items_from_character(self, character: str):
        items = []
        for index in self.items:
            item = self.items[index]
            if item.character is None:
                return items

            if item.character.lower() == character.lower():
                items.append(item)

        return items
