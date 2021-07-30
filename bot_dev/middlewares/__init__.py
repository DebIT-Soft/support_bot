from middlewares.is_banned import IsBanned
from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    # dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(IsBanned())
