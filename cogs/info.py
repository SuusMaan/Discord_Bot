# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

def create_embed(title=None, description=None, color=discord.Color.blue(), fields=None, footer_text=None, footer_icon_url=None, image_url=None, thumbnail_url=None):
    """Создает embed с возможностью настройки цвета, footer, полей, изображения и thumbnail."""
    embed = discord.Embed(title=title, description=description, color=color)
    if fields:
        for field in fields:
            embed.add_field(**field)
        if footer_text:
            embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        if image_url:
            embed.set_image(url=image_url)
        if thumbnail_url:
            embed.set_thumbnail(url=thumbnail_url)
    return embed

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", help="Показывает информацию о разработчике и полезные ссылки.")
    async def info(self, ctx):  # Изменили info_command на info
        """Отображает информацию о разработчике и ссылки."""
        embed = create_embed(
            title="Информация",
            description="Полезные ссылки и информация о разработчике.",
            color=discord.Color.gold(),
            fields=[
                {"name": "GitHub", "value": "[GitHub SusMan-а](https://github.com/SuusMaan)", "inline": False},
                {"name": "YouTube", "value": "[Творчество Кентовки](https://www.youtube.com/@Sus_Man_Kentovka)", "inline": False},
                {"name": "Discord Server", "value": "[Связь в Кентовкой](https://discord.gg/7Y7uu4RY5r)", "inline": False},
                {"name": "Поддержать проект", "value": "[Ссылка на ваш Patreon/DonationAlerts](https://www.patreon.com/your_patreon)", "inline": False},
                {"name": "Веб-сайт", "value": "[Ссылка на ваш веб-сайт](https://your_website.com)", "inline": False},
            ],
            footer_text=f"Запрошено пользователем {ctx.author.name}",
            footer_icon_url=ctx.author.avatar
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()  # Удаляем сообщение пользователя

async def setup(bot):
    await bot.add_cog(InfoCog(bot))