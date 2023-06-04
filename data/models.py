from dataclasses import dataclass

from functools import cached_property

import typing

BASE_PATH = "./data/assets/characters/"


class UnregisteredDataManager:
    pass


class UnregisteredError(Exception):
    pass


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

    instance: typing.Any = UnregisteredDataManager()

    def __post_init__(self):
        print(f"{self.name} has been created")


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
    type: str
    level: typing.Union[int, str]
    image: str
    juice: int
    character: str

    instance: typing.Any = UnregisteredDataManager()

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

    instance: typing.Any = UnregisteredDataManager()

    def __str__(self):
        return self.name


@dataclass
class DataManagerBase:
    enemies: typing.Dict[int, Enemy] = None
    items: typing.Dict[int, Item] = None
    skills: typing.Dict[int, Skill] = None
    characters: typing.Dict[int, Character] = None
    
    @cached_property
    def list_characters(self):
        return [character.name for character in self.characters.values()]

    