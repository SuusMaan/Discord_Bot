from discord.ext import commands

async def setup(bot):
    await bot.add_cog(ModerationCog(bot)) # Замените ModerationCog на название вашего класса

class ModerationCog(commands.Cog): # Замените ModerationCog на название вашего класса
    def __init__(self, bot):
        self.bot = bot
        # ... ваш код ...