from aiogram import Dispatcher

from app.config import Config


def register_middlewares(dp: Dispatcher, config: Config):
    from . import throttling, register_user

    throttling.register_middleware(dp=dp, config=config)
    register_user.register_middleware(dp=dp)
