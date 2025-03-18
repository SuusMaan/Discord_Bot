# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import requests
import json
import asyncio
from cogs.commands.fun import create_embed  # Импортируем create_embed

load_dotenv()

AIML_API_KEY = os.environ.get("AIML_API_KEY")
AIML_API_URL = "https://api.aimlapi.com/v1/chat/completions"

class AIMLIntegrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generating = False
        self.max_response_length = 1900  # Увеличиваем максимальную длину ответа

    @commands.command(name="gpt", help="Задает вопрос AI.")
    async def gpt(self, ctx, *, question):
        if self.generating:
            await ctx.send("В данный момент обрабатывается другой запрос. Пожалуйста, подождите.")
            return

        self.generating = True
        try:
            # Удаление сообщения пользователя (важно сделать это в начале)
            await ctx.message.delete()

            processing_embed = discord.Embed(
                title="Обработка запроса",
                description="Пожалуйста, подождите...",
                color=discord.Color.yellow()
            )
            processing_embed.set_footer(
                text="AIML API",
                icon_url="https://example.com/aiml_logo.png"  # Замените на реальную ссылку
            )
            processing_message = await ctx.send(embed=processing_embed)  # Отправляем сообщение "Обработка запроса"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AIML_API_KEY}"
            }

            data = {
                "messages": [
                    {"role": "user", "content": question}
                ],
                "model": "gpt-3.5-turbo",  # Или другая модель, которую вы используете
            }

            response = requests.post(AIML_API_URL, headers=headers, data=json.dumps(data))
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code == 429:
                embed = discord.Embed(
                    title="Превышен лимит",
                    description="У меня закончились токены. Пожалуйста, подождите около часа.",
                    color=discord.Color.red()
                )
                await processing_message.edit(embed=embed)
                return

            response_json = response.json()

            if "choices" in response_json and len(response_json["choices"]) > 0:
                answer = response_json["choices"][0]["message"]["content"]

                # Формируем базовый Embed
                embed = discord.Embed(
                    title="Кентовка Лидер отвечает: ",
                    color=discord.Color.green(),
                )
                embed.set_footer(
                    text=f"Запрошено пользователем {ctx.author.name}",
                    icon_url=ctx.author.avatar.url
                )

                # Добавляем запрос пользователя (Запрос пользователя:)
                embed.add_field(name="Запрос пользователя:", value=question, inline=False)

                # Разделение ответа, если он слишком длинный
                if len(answer) > self.max_response_length:
                    parts = [answer[i:i + self.max_response_length] for i in range(0, len(answer), self.max_response_length)]
                    for i, part in enumerate(parts):
                        embed_part = embed.copy()  # Создаем копию Embed, чтобы не перезаписывать
                        embed_part.description = part
                        embed_part.title = f"Кентовка Лидер отвечает (часть {i+1}/{len(parts)})"
                        await ctx.send(embed=embed_part)  # Отправляем отдельные сообщения в чат
                    await processing_message.delete()  # Удаляем сообщение "Обработка запроса"

                else:
                    embed.description = answer
                    await processing_message.edit(embed=embed)  # Изменяем сообщение "Обработка запроса"
            else:
                embed = discord.Embed(
                    title="Ошибка AIML API",
                    description=f"Не удалось получить ответ: {response_json}",
                    color=discord.Color.red()
                )
                await processing_message.edit(embed=embed)  # Изменяем сообщение "Обработка запроса"

        except Exception as e:
            print(f"Ошибка при обращении к AIML API: {e}")
            embed = discord.Embed(
                title="Произошла ошибка",
                description=f"При обработке запроса произошла ошибка: {e}",
                color=discord.Color.red()
            )
            await processing_message.edit(embed=embed)  # Изменяем сообщение "Обработка запроса"
        finally:
            self.generating = False

async def setup(bot):
    await bot.add_cog(AIMLIntegrationCog(bot))