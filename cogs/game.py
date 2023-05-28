from typing import List
from discord import app_commands
from discord.ext import commands
import discord


class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="skills", description="Show you details about OMORI skills in-game")
    async def skills(self, inter: discord.Interaction):
        embed = discord.Embed(
            title="OMORI Skills",
            color=discord.Color.red()
        )

        for index in self.bot.data.skills:
            skill = self.bot.data.skills[index]
            embed.add_field(
                name=f"{index + 1}. {skill.name}",
                value=f"Description: **{skill.description}**")

        await inter.response.send_message(embed=embed)

    @app_commands.command(name="characters", description="Shows the OMORI game characters information.")
    async def characters(self, inter: discord.Interaction, name: str):
        
        character = await self.bot.data.find_character_by_name(name)

        if character is None:
            await inter.response.send_message("`🚨 | This character does not exist!`", ephemeral=True)
            return

        embed = discord.Embed(
            title=character.name,
            description=character.description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=character.image)

        embed.add_field(name="Birthday", value=f"{character.birthday} <t:{character.BD_UNIX}:R>")

        await inter.response.send_message(embed=embed)


    @characters.autocomplete("name")
    async def characters_ac(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        characters = self.bot.data.characters

        suggestions = []

        for index in characters:
            print(index)
            character = characters[index]
            print(character)
            suggestions.append(app_commands.Choice(name=character.name, value=character.BD_UNIX))

        print(suggestions)

        return suggestions


async def setup(bot):
    await bot.add_cog(GameCommands(bot))
