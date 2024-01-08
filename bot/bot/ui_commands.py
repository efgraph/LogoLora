from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="generate", description="Generate logo with prompts"),
        BotCommand(command="clear", description="Clear generation history"),
        BotCommand(command="howto", description="Describe bot commands"),
        BotCommand(command="rate", description="Rate logo with offset"),
        BotCommand(command="history", description="View generated logo with offset"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
