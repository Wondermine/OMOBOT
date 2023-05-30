from discord import app_commands
from discord.ext import commands
import discord


from typing import Optional

from base import OMOBOT


class GameCommands(commands.Cog):
    def __init__(self, bot: OMOBOT):
        self.bot = bot

    @app_commands.command(name="skills", description="Show you details about OMORI skills in-game")
    async def skills(self, inter: discord.Interaction, name: Optional[str]):
        embed = discord.Embed(
            title="OMORI game Skills",
            color=discord.Color.red()
        )

        if name is None:
            for index in self.bot.data.skills:
                skill = self.bot.data.skills[index]
                embed.add_field(
                    name=f"{index + 1}. {skill.name}",
                    value=f"Description: **{skill.description}**"
                )

        else:
            skill = await self.bot.data.find_skill_by_name(name)
            if skill is None:
                return await inter.response.send_message("`🚨 | This skill does not exist!`", ephemeral=True)

            embed.add_field(
                name=f"{skill.name}",
                value=f"**description:**\n{skill.description}",
                inline=False
            )

            embed.add_field(
                name="Character",
                value=f"**{self.bot.data.characters[skill.character].name}**",
                inline=False
            )

            embed.add_field(
                name="juice",
                value=f"{skill.juice} <:__:1112092849748594719>",
                inline=False
            )

            embed.add_field(
                name=f"Level",
                value=skill.level,
                inline=False
            )

            embed.set_thumbnail(url=self.bot.data.characters[skill.character].image)

            if skill.image is None:
                embed.set_image(url="https://i.ibb.co/mFK38Tj/notfound.gif")
            else:
                embed.set_image(url=skill.image)

        await inter.response.send_message(embed=embed)

    @app_commands.command(name="characters", description="Shows the OMORI game characters information.")
    async def characters(self, inter: discord.Interaction, name: str = None):
        
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

async def setup(bot: OMOBOT):
    await bot.add_cog(GameCommands(bot))
