from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update

from app.db.functions import User


class RegisterUser(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        if not await User.is_registered(user_id):
            await User.register(user_id)
        return await handler(event, data)


def register_middleware(dp: Dispatcher):
    throttling_middleware = RegisterUser()
    dp.message.middleware(throttling_middleware)
