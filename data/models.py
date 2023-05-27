from functools import cached_property

from dataclasses import dataclass

import typing


class UnregisteredDataManager:
    pass


class UnregisteredError(Exception):
    pass

@dataclass
class Character:
    id: int
    name: str
    description: str
    world: int
    frame_image: str
    skills: list

@dataclass
class Item:
    id: int
    name: str
    description: str
    world: int
    cost: int
    image: str

    instance: typing.Any = UnregisteredDataManager()

    def __str__(self):
        return self.name


@dataclass
class Skill:
    id: int
    name: str
    level: int
    world: int
    description: str
    image: str
    animation: str
    juice: int
    character: int


@dataclass
class Enemies:
    id: int
    name: str
    world: int
    stage: int
    description: str
    image: str
    animation: str
    health: int
    max_health: int
    damage: int
    defense: int
    skills: list
