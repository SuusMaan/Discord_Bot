# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import os
import requests
import json
from dotenv import load_dotenv
from cogs.commands.fun import create_embed

load_dotenv()

AIML_API_KEY = os.environ.get("AIML_API_KEY")
AIML_API_URL = "https://api.aimlapi.com/v1/chat/completions"

class AIMLIntegrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generating = False

    @commands.command(name="gpt", help="Задает вопрос AI.")
    async def gpt(self, ctx, *, question):
        if self.generating:
            await ctx.send("В данный момент обрабатывается другой запрос. Пожалуйста, подождите.")
            return

        self.generating = True
        try:
            processing_embed = create_embed(
                title="Обработка запроса",
                description="Пожалуйста, подождите...",
                color=discord.Color.yellow(),
                footer_text="AIML API",
                footer_icon_url="https://example.com/aiml_logo.png"
            )
            processing_message = await ctx.message.reply(embed=processing_embed)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AIML_API_KEY}"
            }

            data = {
                "model": "gpt-4",
                "messages": [{"role": "user", "content": question}]
            }

            response = requests.post(AIML_API_URL, headers=headers, data=json.dumps(data))
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code == 429:
                embed = create_embed(
                    title="Превышен лимит",
                    description="У меня закончились токены. Пожалуйста, подождите около часа.",
                    color=discord.Color.red()
                )
                await processing_message.edit(embed=embed)
                return

            response_json = response.json()

            if "choices" in response_json and len(response_json["choices"]) > 0:
                answer = response_json["choices"][0]["message"]["content"]
                embed = create_embed(
                    title="Кентовка Лидер отвечает: ",
                    description=answer,
                    color=discord.Color.green(),
                    fields=[
                        {"name": "Запрос пользователя", "value": question, "inline": False}
                    ],
                    footer_text=f"Запрошено пользователем {ctx.author.name}",
                    footer_icon_url=ctx.author.avatar.url
                )
                await processing_message.edit(embed=embed)
            else:
                embed = create_embed(
                    title="Ошибка AIML API",
                    description=f"Не удалось получить ответ: {response_json}",
                    color=discord.Color.red()
                )
                await processing_message.edit(embed=embed)

        except Exception as e:
            print(f"Ошибка при обращении к AIML API: {e}")
            embed = create_embed(
                title="Произошла ошибка",
                description=f"При обработке запроса произошла ошибка: {e}",
                color=discord.Color.red()
            )
            await processing_message.edit(embed=embed)
        finally:
            self.generating = False

async def setup(bot):
    await bot.add_cog(AIMLIntegrationCog(bot))