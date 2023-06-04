from data import models
from . import models

import csv
import json

from pathlib import Path

from .models import Character


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
    path = Path(__file__).parent / "json" / filename

    with open(path) as f:
        raw_data = json.loads(f.read())

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
            character=skill_obj["character"],
            instance=instance
        )

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
    data = get_data_from_json("characters.json")

    characters = {}

    for character_name in data["DreamWorld"]:

        character = data["DreamWorld"][character_name]

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
            image=character["image"],
            instance=instance
        )

    return characters


class DataManager(models.DataManagerBase):
    def __init__(self):
        # self.items = get_items(self)
        self.skills = get_skills(self)
        # self.enemies = get_enemies(self)
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

    async def find_skills_from_character(self, character: str):
        skills = []
        for index in self.skills:
            skill = self.skills[index]
            if skill.character.lower() == character.lower():
                skills.append(skill)

        return skills
