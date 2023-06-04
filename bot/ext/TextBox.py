import discord

from discord.ext.commands import GroupCog

from discord import app_commands

from bot.bot import OMOBOT

import io

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import enum


class Characters(enum.Enum):
    OMORI = "OMORI"
    KEL = "KEL"
    AUBREY = "AUBREY"
    HERO = "HERO"
    BASIL = "BASIL"
    MARI = "MARI"


class Expressions(enum.Enum):
    idle = "idle"
    happy = "happy"
    sad = "sad"


def text_splitter(text: str):

    texts_list = [[], [], []]

    text_listed = text.split(" ")

    # max letters each is 64

    destination = 0

    char_count = 0

    for word in text_listed:

        if char_count in [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67]:
            destination = 1
            texts_list[1].append(word)
            char_count += len(word) + 1
            continue

        if char_count in [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131]:
            destination = 2
            texts_list[2].append(word)
            char_count += len(word) + 1
            continue

        char_count += len(word) + 1

        texts_list[destination].append(word)

    text1 = " ".join(texts_list[0])
    text2 = " ".join(texts_list[1])
    text3 = " ".join(texts_list[2])

    print(text1)
    print(text2)
    print(text3)

    return [text1, text2, text3]


# noinspection PyUnresolvedReferences
class TextBoxGenerator(
    GroupCog,
    name="text",
    description="Generates OMORI game themed textbox. Animated and static..."
):
    def __init__(self, bot: OMOBOT):
        self.bot = bot
        self.base_font = ImageFont.truetype("./data/fonts/OMORI_GAME.ttf", 30)
        self.base_path = "./data/assets/characters/"

    @app_commands.command(name="animated", description="Gives an animated (moving) text box with everything you need.")
    @app_commands.describe(character='Choose a character', expression='Choose a an expression')
    @app_commands.checks.cooldown(1, 120.0)
    async def animated(
            self,
            inter: discord.Interaction,
            text: str,
            character: Characters,
            expression: Expressions
    ):

        if len(text) > 202:
            await inter.response.send_message("That is too much talkin'", ephemeral=True)
            return

        if character.value == "OMORI":
            if expression.value != "idle":
                await inter.response.send_message(
                    "OMORI doesn't have that expression, he only has an idle one...",
                    ephemeral=True
                )
                return

        if character.value == "MARI":
            if expression.value == "sad":
                await inter.response.send_message(
                    "MARI can never be sad it seems... she has a smug though",
                    ephemeral=True
                )
                return

        await inter.response.send_message("generating...", ephemeral=True)

        texts = text_splitter(text)

        prev_im = Image.open("./data/assets/base/input.png")
        portrait = Image.open(self.base_path + character.value + f"/{expression.value}0.png")

        gif = []

        pixel = [10.0, 130.0]

        checks = True

        count = -1
        for index in texts:
            count += 1

            if count == 1:
                pixel[0] = 10
                pixel[1] += 28

            if count == 2:
                pixel[0] = 10
                pixel[1] += 28

            for i in range(len(index)):
                temp_im = prev_im.copy()

                d = ImageDraw.Draw(temp_im)

                while checks:
                    size = d.textlength(character.value, font=self.base_font)

                    x_axis = size + 25

                    d.rectangle((0, 70, x_axis, 114), fill=(255, 255, 255), width=1, outline=(0, 0, 0))

                    # 4 pixels difference

                    d.rectangle((4, 74, x_axis - 4, 110), fill=(0, 0, 0), width=1)

                    d.text((12, 76), character.value, font=self.base_font, fill=(255, 255, 255))
                    temp_im.paste(portrait, (498, 4), portrait)
                    checks = False

                d.text(tuple(pixel), texts[count][i], font=self.base_font, fill=(255, 255, 255))

                size = d.textlength(texts[count][i], font=self.base_font)

                pixel[0] += size
                prev_im = temp_im.copy()
                temp_im.filter(ImageFilter.SMOOTH_MORE)

                if texts[count][i] == ".":
                    try:
                        if texts[count][i+1] == " " and texts[count][i-1] != ".":
                            for num in range(20):
                                gif.append(temp_im)
                            continue
                        gif.append(temp_im)
                    except IndexError:
                        gif.append(temp_im)

                else:
                    gif.append(temp_im)

        arr = io.BytesIO()
        gif[0].save(arr, format="GIF", duration=25, disposal=2, save_all=True, append_images=gif[1:])
        arr.seek(0)

        file = discord.File(arr, filename="response.gif")

        await inter.followup.send(content=inter.user.mention, file=file)

    @app_commands.command(
        name="static",
        description="Gives a static (still) image of a text box with everything you need."
    )
    @app_commands.checks.cooldown(1, 20.0)
    @app_commands.describe(character='Choose a character', expression='Choose a an expression')
    async def static_generator(
            self,
            inter: discord.Interaction,
            text: str,
            character: Characters,
            expression: Expressions
    ):

        if len(text) > 202:
            await inter.response.send_message("That is too much talkin'", ephemeral=True)
            return

        await inter.response.send_message("generating...", ephemeral=True)

        texts = text_splitter(text)

        image = Image.open("./data/assets/base/input.png")
        portrait = Image.open(self.base_path + character.value + f"/{expression.value}0.png")

        d = ImageDraw.Draw(image)

        # name space rectangle
        size = d.textlength(character.value, font=self.base_font)

        x_axis = size + 25

        d.rectangle((0, 70, x_axis, 114), fill=(255, 255, 255), width=1, outline=(0, 0, 0))

        d.rectangle((4, 74, (x_axis - 4), 110), fill=(0, 0, 0), width=1)

        y = 130
        count = -1
        for index in texts:
            count += 1

            if count == 1:
                y += 28

            if count == 2:
                y += 28

            d.text((10, y), index, font=self.base_font, fill=(255, 255, 255))

        d.text((12, 76), character.value, font=self.base_font, fill=(255, 255, 255))
        image.paste(portrait, (498, 4), portrait)

        arr = io.BytesIO()

        image.filter(ImageFilter.SMOOTH_MORE)

        image.save(arr, format='PNG')

        arr.seek(0)
        file = discord.File(arr, filename="response.png")

        await inter.followup.send(file=file)


async def setup(bot: OMOBOT):
    await bot.add_cog(TextBoxGenerator(bot))
