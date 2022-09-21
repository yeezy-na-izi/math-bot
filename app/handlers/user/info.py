from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.commands import bot_commands, matrix_commands, logic_commands, admin_commands, for_teacher_command
from app.config import Config
from app.keyboards.inline import get_author_keyboard

router = Router()


@router.message(Command(commands=["help"]))
async def help_handler(message: Message, config: Config):
    text = "ℹ️ <b>Список команд:</b> \n\n"
    text += "<b>🤖 Команды бота:</b> \n"
    for command in bot_commands:
        text += f"/{command} - {bot_commands[command]} \n"
    text += "\n"
    text += "<b>📐 Команды для работы с матрицами:</b> \n"
    for command in matrix_commands:
        text += f"/{command} - {matrix_commands[command]} \n"
    text += "\n"
    text += "<b>🧠 Команды для работы с логическими выражениями:</b> \n"
    for command in logic_commands:
        text += f"/{command} - {logic_commands[command]} \n"
    text += "\n"
    # add commands for teacher
    text += "<b> Команды для учителя:</b> \n"
    for command in for_teacher_command:
        text += f"/{command} - {for_teacher_command[command]} \n"
    text += "\n"

    if message.from_user.id == config.settings.owner_id:
        text += "<b>👑 Команды для владельца:</b> \n"
        for command in admin_commands:
            text += f"/{command} - {admin_commands[command]} \n"
        text += "\n"

    await message.answer(text)


@router.message(Command(commands=["about"]))
async def about_handler(message: Message, bot: Bot, config: Config):
    bot_information = await bot.get_me()
    await message.answer(
        "<b>ℹ️ Информация о боте:</b> \n\n"
        f"<b>Название - </b> {bot_information.full_name} \n"
        f"<b>Username - </b> @{bot_information.username} \n"
        f"<b>ID - </b> <code>{bot_information.id}</code> \n",
        reply_markup=get_author_keyboard(owner_id=config.settings.owner_id),
    )
