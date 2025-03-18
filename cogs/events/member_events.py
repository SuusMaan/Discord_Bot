import discord
from discord.ext import commands

class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Привет, {member.mention}! Добро пожаловать на сервер!")

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))