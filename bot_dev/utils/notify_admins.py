import logging

from aiogram import Dispatcher
from time import time

from data.config import ADMINS, USERS

from aiogram_broadcaster import TextBroadcaster


async def on_startup_notify(dp: Dispatcher):
    await TextBroadcaster(ADMINS, '🛠 Привет, я снова работаю, в данный момент загружаю модули :)').run()