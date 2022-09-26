from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.functions import User
from app.filters.is_owner import IsOwner

router = Router()


@router.message(IsOwner(is_owner=True), Command(commands=["stats"]))
async def stats_handler(message: Message):
    count = await User.get_count()
    await message.answer(
        f"📊 <b>Количество пользователей бота -</b> <code>{count}</code>"
    )


@router.message(IsOwner(is_owner=True), Command(commands=["users"]))
async def users_handler(message: Message):
    await message.reply(
        "📊 <b>Список пользователей бота -</b> "
    )
    users = await User.all()
    for user in users:
        try:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="Пользователь", url=f"tg://user?id={user.telegram_id}")
            await message.answer(str(user), reply_markup=keyboard.as_markup())
        except Exception as e:
            await message.answer(str(user))
