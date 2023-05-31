import discord

from discord.ext import commands

from discord import app_commands

from base import OMOBOT

import io

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageSequence

from typing import Optional


def text_splitter(text: str):

    texts_list = [[], [], []]

    text_listed = text.split(" ")

    # max letters each is 64

    destination = 0

    char_count = 0

    for word in text_listed:

        if char_count in [60, 61, 62, 63, 64]:
            destination = 1
            texts_list[1].append(word)
            char_count += len(word) + 1
            continue

        if char_count in [123, 124, 125, 126, 127, 128]:
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


class TextBoxGenerator(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot
        self.base_font = ImageFont.truetype("./data/fonts/OMORI_GAME.ttf", 28)

    @app_commands.command(name="generate", description="generates OMORI text")
    async def generate(self, inter: discord.Interaction, text: str):

        await inter.response.send_message("generating...", ephemeral=True)

        if len(text) > 202:
            await ctx.send("That is too much talkin'")
            return

        texts = text_splitter(text)

        prev_im = Image.open("./data/assets/base/input.png")

        gif = []

        pixel = [10.0, 130.0]

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

                d.text(tuple(pixel), texts[count][i], font=self.base_font, fill=(255, 255, 255))
                size = d.textlength(texts[count][i], font=self.base_font)

                pixel[0] += size
                prev_im = temp_im.copy()
                temp_im.filter(ImageFilter.SMOOTH_MORE)

                gif.append(temp_im)

        arr = io.BytesIO()
        gif[0].save(arr, format="GIF", duration=20, disposal=2, save_all=True, append_images=gif[1:])
        arr.seek(0)

        file = discord.File(arr, filename="response.gif")

        await inter.followup.send(content=inter.user.mention, file=file)

    # @app_commands.command(name="textbox", description="generates OMORI textbox image")
    # @app_commands.guilds(discord.Object(id=1110803661988311112))
    @commands.command()
    async def textbox(self, ctx: commands.Context, *, text: str):

        if len(text) > 202:
            await ctx.send("That is too much talkin'")
            return

        texts = text_splitter(text)

        image = Image.open("./data/assets/base/input.png")

        d = ImageDraw.Draw(image)

        y = 129
        count = -1
        for index in texts:
            count += 1

            if count == 1:
                y += 28

            if count == 2:
                y += 28

            d.text((19, y), index, font=self.base_font, fill=(255, 255, 255))

        arr = io.BytesIO()

        image.filter(ImageFilter.SMOOTH_MORE)

        image.save(arr, format='PNG')

        arr.seek(0)
        file = discord.File(arr, filename="response.png")

        await ctx.send(file=file)


async def setup(bot: OMOBOT):
    await bot.add_cog(TextBoxGenerator(bot))
