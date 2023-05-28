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
    description: str
    type: int
    level: int
    image: str
    juice: int
    character: int

    instance: typing.Any = UnregisteredDataManager()


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

    instance: typing.Any = UnregisteredDataManager()

@dataclass
class DataManagerBase:
    enemies: typing.Dict[int, Enemy] = None
    items: typing.Dict[int, Item] = None
    skills: typing.Dict[int, Skill] = None
    characters: typing.Dict[int, Character] = None

    def all_enemies(self):
        return self.enemies.values()

    def all_items(self):
        return self.items.values()
