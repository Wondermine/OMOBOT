# from dataclasses import dataclass
import typing

from data import models
from . import models

import csv

from pathlib import Path

from .models import Character


BASE_PATH = "./data/assets/characters/"


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


def get_items(instance):
    items_data = get_data_from("items.csv")

    items = {}

    for row in items_data:
        items[row["id"]] = models.Item(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            world=row["world"],
            cost=row["cost"],
            image=row["image"],
            instance=instance
        )
    return items


def get_skills(instance):
    skills_data = get_data_from("skills.csv")

    skills = {}

    for row in skills_data:
        skill = models.Skill(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            type=row["type"],
            level=row["level"],
            juice=row["juice"],
            image=row["image"],
            character=row["character"],
            instance=instance
        )

        if row["image"] == "null":
            skill.image = None

        skills[row["id"]] = skill

    return skills


def get_enemies(instance):
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
            skills=row["skills"],
            instance=instance
        )
    return enemies


def get_characters(instance):
    characters_data = get_data_from("characters.csv")

    characters = {}

    for row in characters_data:
        characters[row["id"]] = models.Character(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            gender=row["gender"],
            age=row["age"],
            birthday=row["birthday"],
            BD_UNIX=row["BD_UNIX"],
            location=row["location"],
            image=row["image"]
        )
        characters[row["id"]].idle = BASE_PATH + characters[row["id"]].name.capitalize() + "/idle.png"

    return characters


class DataManager(models.DataManagerBase):
    def __init__(self):
        self.items = get_items(self)
        self.skills = get_skills(self)
        self.enemies = get_enemies(self)
        self.characters = get_characters(self)

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
