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
    data = get_data_from("items.csv")

    items = {}

    for row in data:
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
    data = get_data_from("skills.csv")

    skills = {}

    for row in data:
        skills[row["id"]] = models.Skill(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            world=row["world"],
            level=row["level"],
            image=row["image"],
            animation=row["animation"],
            juice=row["juice"],
            character=row["character"],
            instance=instance
        )
    return skills

def get_enemies(instance):
    data = get_data_from("enemies.csv")

    enemies = {}

    for row in data:
        enemies[row["id"]] = models.Enemy(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            world=row["world"],
            stage=row["stage"],
            image=row["image"],
            animation=row["animation"],
            health=row["health"],
            max_health=row["max_health"],
            damage=row["damage"],
            defense=row["defense"],
            skills=row["skills"],
            instance=instance
        )
    return enemies


class DataManager(models.DataManagerBase):
    def __init__(self):
        self.items = get_items(self)
        self.skills = get_skills(self)
        self.enemies = get_enemies(self)
