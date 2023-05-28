# from dataclasses import dataclass

from . import models

import csv

from pathlib import Path


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
        data = list(
            {k: int(v) if isnumber(v) else v for k, v in row.items() if v != ""}
            for row in reader
        )

    return data


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


class DataManager(models.DataManagerBase):
    def __init__(self):
        self.items = get_items(self)
        self.skills = get_skills(self)
        self.enemies = get_enemies(self)
