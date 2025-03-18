# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import random
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env

# --- Вспомогательные функции для создания Embed ---
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

# Ваши списки
roasts = [
    "Эй, {user}, твой код выглядит так, будто его писал пьяный енот.",
    "{user}, ты настолько тупой, что мог бы спорить с камнем и проиграть.",
    "Извини, {user}, но у тебя мозгов, как у креветки."
]

responses = [
    "Да, это так.",
    "Нет, это невозможно.",
    "Возможно, но маловероятно.",
    "Спросите позже, я занят.",
    "Лучше вам не знать.",
    "Сконцентрируйтесь и спросите снова.",
    "Не уверен, это сложный вопрос.",
    "Однозначно да!",
    "Однозначно нет!",
    "Может быть."
]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello", help="Приветствует пользователя.")
    async def hello(self, ctx):
        """Отправляет приветственное сообщение."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        embed = create_embed(
            title="Привет, я Кентовка Лидер!",  # Более информативный заголовок
            description="Я предназначен для частного использования членами Кентовки SusMan-а.",
            color=discord.Color.green(),
            thumbnail_url="https://tools.corenexis.com/image/cnxm/M25/03/a1df7927f3.webp",  # Добавим картинку
            fields=[
                {"name": "Разработчик", "value": "SusMan", "inline": False},
                {"name": "Версия", "value": "1.0", "inline": True},
                {"name": "Префикс", "value": f"`{ctx.prefix}`", "inline": True}  # Добавили информацию о префиксе
            ],
            footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
            footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
        )
        await ctx.send(embed=embed)

    @commands.command(name="ping", help="Показывает задержку бота.")
    async def ping(self, ctx):
        """Показывает задержку бота."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        embed = create_embed(
            title="Понг!",
            description=f"Задержка: {round(self.bot.latency * 1000)}мс",
            color=discord.Color.blue(),
            footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
            footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
        )
        await ctx.send(embed=embed)

    @commands.command(name="say", help="Повторяет текст, который вы введете.")
    async def say(self, ctx, *, text):
        """Повторяет введенный текст."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        embed = create_embed(
            description=text,
            color=discord.Color.orange(),
            footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
            footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
        )
        await ctx.send(embed=embed)

    @commands.command(name="roast", help="Оскорбляет указанного пользователя.")
    async def roast(self, ctx, user: discord.Member = None):
        """Оскорбляет пользователя (или автора сообщения)."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        if user is None:
            user = ctx.author
        roast_text = random.choice(roasts).format(user=user.mention)
        embed = create_embed(
            description=roast_text,
            color=discord.Color.dark_red(),
            footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
            footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
        )
        await ctx.send(embed=embed)

    @commands.command(name="ask", help="Отвечает на ваш вопрос случайным образом.")
    async def ask(self, ctx, *, question):
        """Отвечает на вопрос случайным образом."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        answer = random.choice(responses)
        embed = create_embed(
            title=f"Вопрос: {question}",
            description=f"Ответ: {answer}",
            color=discord.Color.purple(),
            footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
            footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
        )
        await ctx.send(embed=embed)

    @commands.command(name="meme", help="Отправляет случайный мем. Можно указать ключевое слово для поиска.")
    async def meme(self, ctx, *, search_term: str = None):
        """Отправляет случайный мем из Imgur.com. Если указан search_term, ищет мемы по ключевому слову."""
        await ctx.message.delete()  # Удаляем сообщение с командой
        # Получаем API-ключ Imgur из переменной окружения
        IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")

        if not IMGUR_CLIENT_ID:
            await ctx.send("Необходимо настроить API-ключ Imgur (IMGUR_CLIENT_ID) в .env.")
            return

        headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
        try:
            if search_term:
                # Если указан поисковый запрос
                url = f"https://api.imgur.com/3/gallery/search?q={search_term}"
            else:
                # Если нет поискового запроса, получаем случайные мемы из раздела 'hot'
                url = "https://api.imgur.com/3/gallery/hot?viral=true&mature=false&album_previews=true"

            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Проверка на HTTP ошибки

            data = response.json()

            if not data["data"]:
                await ctx.send("Ничего не найдено по вашему запросу.")
                return

            # Выбираем случайный элемент из результатов
            images = [item for item in data["data"] if 'images' in item and item['images']]
            if not images:
                images = data["data"]

            meme = random.choice(images)

            if 'images' in meme:
                image = random.choice(meme['images'])
                image_url = image['link']
                meme_title = meme['title']
            else:
                image_url = meme['link']
                meme_title = meme['title']
            embed = create_embed(
                title=meme_title,
                color=discord.Color.blurple(),
                image_url=image_url,
                footer_text=f"Запрошено {ctx.author.name}",  # Добавляем информацию о пользователе
                footer_icon_url=ctx.author.avatar.url  # Добавляем аватар пользователя
            )
            await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к Imgur API: {e}")
            await ctx.send("Не удалось получить мем (ошибка API).")
        except (KeyError, IndexError) as e:
            print(f"Ошибка при обработке данных: {e}")
            await ctx.send("Не удалось получить мем (ошибка данных).")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            await ctx.send("Произошла неизвестная ошибка.")

async def setup(bot):
    await bot.add_cog(Fun(bot))