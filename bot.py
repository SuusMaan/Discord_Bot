import discord
from discord.ext import commands
import os
from utils import config  # Импортируем настройки из utils/config.py
import asyncio  # Импортируем модуль asyncio
import traceback  # Импортируем traceback

# Настройка intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Если нужны события, связанные с участниками
intents.guilds = True  # Добавляем guilds intent

# Создание бота
bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

def create_red_embed(title=None, description=None, fields=None, image_url=None):
    """Создает красный embed."""
    embed = discord.Embed(color=discord.Color.red())
    if title:
        embed.title = title
    if description:
        embed.description = description
    if fields:
        for field in fields:
            embed.add_field(**field)
    if image_url:
        embed.set_image(url=image_url)
    return embed

# Загрузка Cogs
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: cogs.{cog_name}")
            except Exception as e:
                print(f"Failed to load extension cogs.{cog_name}: {e}")
                traceback.print_exc()

    for folder in os.listdir("./cogs"):
        if os.path.isdir(f"./cogs/{folder}"):
            for filename in os.listdir(f"./cogs/{folder}"):
                if filename.endswith(".py"):
                    cog_name = filename[:-3]
                    try:
                        await bot.load_extension(f"cogs.{folder}.{cog_name}")
                        print(f"Loaded cog: cogs.{folder}.{cog_name}")
                    except Exception as e:
                        print(f"Failed to load extension cogs.{folder}.{cog_name}: {e}")
                        traceback.print_exc()


# Обработка неправильных команд
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(config.COMMAND_PREFIX): # Используем префикс из config.py
        ctx = await bot.get_context(message)
        if ctx.command is None:
            embed = create_red_embed(
                title="Неизвестная команда",
                description=f"Такой команды не существует. Используйте `{config.COMMAND_PREFIX}help` для просмотра списка доступных команд."
            )
            await ctx.send(embed=embed)

    await bot.process_commands(message)  # Обрабатываем команды как обычно

# Обработчик on_interaction
@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        await interaction.response.defer()  # Подтверждаем получение взаимодействия
    except discord.errors.NotFound:
        print("Interaction not found")  # Interaction больше не существует

# Событие on_ready
@bot.event
async def on_ready():
    print(f'Бот {bot.user.name} подключился к Discord!')

# Запуск ботаа
async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.TOKEN)  # Используем токен из utils/config.py

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())