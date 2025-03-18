# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.ui import Button, View
from cogs.commands.fun import create_embed  # Импортируем create_embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")  # Удаляем стандартную команду help

    @commands.command(name="help", help="Показывает список команд или информацию о конкретной команде.")
    async def help_command(self, ctx, command_name=None):
        """Отображает список команд или подробную информацию о конкретной команде."""
        await ctx.message.delete()  # Удаляем сообщение пользователя

        if command_name:
            # Информация о конкретной команде (как было раньше)
            command = self.bot.get_command(command_name)
            if command is None:
                embed = self.create_error_embed(ctx, "Такая команда не найдена.")
                await ctx.send(embed=embed)
                return
            embed = self.create_command_help_embed(ctx, command)
            await ctx.send(embed=embed)
        else:
            # Общий список команд с кнопками
            await self.send_help_with_buttons(ctx)

    async def send_help_with_buttons(self, ctx):
        """Отправляет сообщение со списком категорий и кнопками для навигации."""
        # --- Создаем кнопки для каждой категории (Cog) ---
        buttons = []
        for cog_name, cog in self.bot.cogs.items():
            if cog_name != "Help":  # Не показываем кнопку для кога Help
                button_label = cog_name  # По умолчанию используем имя кога

                # Изменяем название кнопки в зависимости от имени кога
                if cog_name == "Fun":
                    button_label = "Развлечения"
                elif cog_name == "ModerationCog":
                    button_label = "Модерация"
                elif cog_name == "InfoCog":
                    button_label = "Информация"
                elif cog_name == "AIMLIntegrationCog":  # Или любое другое имя вашего кога GPT
                    button_label = "AI"

                button = Button(label=button_label, style=discord.ButtonStyle.primary)
                buttons.append(button)

                # --- Создаем колбэк для каждой кнопки ---
                async def button_callback(interaction: discord.Interaction, cog=cog):
                    embed = self.create_category_help_embed(ctx, cog)
                    await interaction.response.edit_message(embed=embed, view=view)  # Передаем view

                button.callback = lambda interaction, cog=cog: button_callback(interaction, cog)

        # --- Создаем View ---
        view = View()
        for button in buttons:
            view.add_item(button)

        # --- Создаем Embed для начального сообщения ---
        initial_embed = self.create_initial_help_embed(ctx)

        # --- Отправляем сообщение с кнопками и первым Embed ---
        await ctx.send(embed=initial_embed, view=view)

    def create_initial_help_embed(self, ctx):
        """Создает Embed для начального сообщения."""
        embed = create_embed(
            title="Список категорий команд",
            description="Нажмите на кнопку, чтобы увидеть список команд в этой категории.",
            color=discord.Color.green(),
            footer_text=f"Запрошено пользователем {ctx.author.name}",
            footer_icon_url=ctx.author.avatar.url
        )
        return embed

    def create_category_help_embed(self, ctx, cog):
        """Создает Embed для отображения команд в категории."""
        commands_list = [command.name for command in cog.get_commands() if not command.hidden]
        if commands_list:
            embed = create_embed(
                title=f"Команды в категории: {cog.__class__.__name__}",
                description=", ".join(commands_list),
                color=discord.Color.blue(),
                footer_text=f"Запрошено пользователем {ctx.author.name}",
                footer_icon_url=ctx.author.avatar.url
            )
        else:
            embed = create_embed(
                title=f"Команды в категории: {cog.__class__.__name__}",
                description="В этой категории нет доступных команд.",
                color=discord.Color.red(),
                footer_text=f"Запрошено пользователем {ctx.author.name}",
                footer_icon_url=ctx.author.avatar.url
            )
        return embed

    def create_command_help_embed(self, ctx, command):
        """Создает Embed для отображения информации о конкретной команде."""
        embed = create_embed(
            title=f"Команда: {command.name}",
            description=command.help or "Нет описания.",
            color=discord.Color.blue(),
            fields=[
                {"name": "Использование", "value": f"`{ctx.prefix}{command.name} {command.signature}`", "inline": False},
                {"name": "Категория", "value": command.cog_name or "Общая", "inline": False}
            ],
            footer_text=f"Запрошено пользователем {ctx.author.name}",
            footer_icon_url=ctx.author.avatar.url
        )
        return embed

    def create_error_embed(self, ctx, description):
        """Создает Embed для отображения ошибки."""
        embed = create_embed(
            title="Ошибка",
            description=description,
            color=discord.Color.red(),
            footer_text=f"Запрошено пользователем {ctx.author.name}",
            footer_icon_url=ctx.author.avatar.url
        )
        return embed

async def setup(bot):
    await bot.add_cog(Help(bot))