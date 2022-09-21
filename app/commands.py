from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from app.config import Config

users_commands = dict()

bot_commands = {
    "help": "Показать список команд",
    "about": "Информация о боте",
}

matrix_commands = {
    "det": "Вычислить детерминант матрицы",
    "inv": "Вычислить обратную матрицу",
    "ref": "Привести матрицу к ступенчатому виду",
    "mul": "Умножить матрицу на матрицу",
}

logic_commands = {
    "logic": "Посчитать логическое выражение",
}

for_teacher_command = {
    "get_random_student": "Получить случайного студента",
}

users_commands.update(bot_commands)
users_commands.update(matrix_commands)
users_commands.update(logic_commands)

admin_commands = {
    "ping": "Check bot ping",
    "stats": "Show bot stats"
}

owner_commands = {**users_commands, **admin_commands}


async def setup_bot_commands(bot: Bot, config: Config):
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in owner_commands.items()
        ],
        scope=BotCommandScopeChat(chat_id=config.settings.owner_id),
    )

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in users_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_bot_commands(bot: Bot, config: Config):
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=config.settings.owner_id)
    )
