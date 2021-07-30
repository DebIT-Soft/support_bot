from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types.message import Message

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(msg: Message):
        await msg.answer('Скоро все будет :)')