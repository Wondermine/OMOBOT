from typing import Callable, Any

import requests

from bs4 import BeautifulSoup
import json
import time

weapons_scrap = requests.get("https://omori.fandom.com/wiki/Category:WEAPONS")
print("scraped weapons")
time.sleep(5)

charms_scrap = requests.get("https://omori.fandom.com/wiki/Category:CHARMS")
print("scraped charms")
time.sleep(5)

snacks_scrap = requests.get("https://omori.fandom.com/wiki/Category:SNACKS")
print("scraped snacks")
time.sleep(5)

toys_scrap = requests.get("https://omori.fandom.com/wiki/Category:TOYS")
print("scraped toys")
time.sleep(5)

important_scrap = requests.get("https://omori.fandom.com/wiki/Category:IMPORTANT_ITEMS")
print("scraped important")

weapons_soup = BeautifulSoup(weapons_scrap.text, "html.parser")
charms_soup = BeautifulSoup(charms_scrap.text, "html.parser")
snacks_soup = BeautifulSoup(snacks_scrap.text, "html.parser")
toys_soup = BeautifulSoup(toys_scrap.text, "html.parser")
important_soup = BeautifulSoup(important_scrap.text, "html.parser")

soups = [
    weapons_soup,
    charms_soup,
    snacks_soup,
    toys_soup,
    important_soup
]

kinds = [
    "weapon",
    "charm",
    "snack",
    "toy",
    "important item"
]

index = 0
idx = 0

items = {}

headline = 0

for soup in soups:
    wiki_tables = soup.find_all(class_="wikitable")

    for wiki_table in wiki_tables:
        world = wiki_table.find_previous("h2").select("span")[0].select("a")[0].text
        print(f"Wikitable for the world {world}")
        stats = wiki_table.find_all("tr")
        stats.pop(0)

        for stat in stats:

            image_url = None
            name = None
            hearts = None
            juice = None
            attack = None
            defense = None
            speed = None
            luck = None
            hit_rate = None
            character = None
            description = None
            cost = None
            kind = kinds[index]

            if world == "UNUSED":
                world = None

            if index == 0:
                image_url = stat.select("td")[0].select("div")[0].select("figure")[0].select("a")[0]["href"]
                name = stat.select("td")[1].select("a")[0].text
                print(f"Setting up item {name}")

                hearts = stat.select("td")[2].text.replace("\n", "")
                juice = stat.select("td")[3].text.replace("\n", "")
                attack = stat.select("td")[4].text.replace("\n", "")
                defense = stat.select("td")[5].text.replace("\n", "")
                speed = stat.select("td")[6].text.replace("\n", "")
                luck = stat.select("td")[7].text.replace("\n", "")
                hit_rate = stat.select("td")[8].text.replace("\n", "")

                character = str(stat.select("td")[9].select("a")[0].text).upper()

                #always exist
                description = str(stat.select("td")[10].text)

            if index == 1:
                image_url = stat.select("td")[0].select("div")[0].select("figure")[0].select("a")[0]["href"]
                name = stat.select("td")[1].select("a")[0].text
                print(f"Setting up item {name}")

                hearts = stat.select("td")[2].text.replace("\n", "")
                juice = stat.select("td")[3].text.replace("\n", "")
                attack = stat.select("td")[4].text.replace("\n", "")
                defense = stat.select("td")[5].text.replace("\n", "")
                speed = stat.select("td")[6].text.replace("\n", "")
                luck = stat.select("td")[7].text.replace("\n", "")
                hit_rate = stat.select("td")[8].text.replace("\n", "")

                description = str(stat.select("td")[9].text)

            if index == 2:
                image_url = stat.select("td")[0].select("div")[0].select("figure")[0].select("a")[0]["href"]
                name = stat.select("td")[1].select("a")[0].text
                print(f"Setting up item {name}")

                hearts = stat.select("td")[2].text.replace("\n", "")
                juice = stat.select("td")[3].text.replace("\n", "")
                cost = stat.select("td")[4].text.replace("\n", "")

                description = str(stat.select("td")[5].text)

            if index == 3:
                image_url = stat.select("td")[0].select("div")[0].select("figure")[0].select("a")[0]["href"]
                name = stat.select("td")[1].select("a")[0].text
                print(f"Setting up item {name}")

                cost = stat.select("td")[2].text.replace("\n", "")

                description = str(stat.select("td")[3].text)

            if index == 4:
                image_url = str(stat.select("td")[0].select("div")[0].select("figure")[0].select("a")[0]["href"])
                try:
                    name = str(stat.select("td")[1].select("a")[0].text)
                except IndexError:
                    name = str(stat.select("td")[1].text)

                description = str(stat.select("td")[2].text)
                print(f"Setting up item {name}")

            item = {
                "id": idx,
                "name": name.replace("\"", "'"),
                "character": character,
                "description": description.replace("\"", "'").replace("\n", ""),
                "world": world,
                "type": kind,
                "image": image_url,
                "hearts": hearts,
                "juice": juice,
                "attack": attack,
                "defense": defense,
                "speed": speed,
                "luck": luck,
                "hit_rate": hit_rate
            }

            items[idx] = item
            idx += 1
    index += 1

with open("data/items.json", "w") as f:
    raw_data = json.dumps(items, indent=4)

    f.write(raw_data)
