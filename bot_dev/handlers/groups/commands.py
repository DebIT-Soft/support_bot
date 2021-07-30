from aiogram.types.message import ContentType, Message
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import ADMINS, SUPPORTS
from aiogram.dispatcher.filters import Text
from aiogram import types
from loader import dp

""" Кикнуть пользователя из чата """
@dp.message_handler(commands='ban')
async def ban_user(msg: Message):
    if msg.from_user.id in ADMINS or msg.from_user.id in SUPPORTS:
        try:
            await dp.bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
        except Exception as e:
            await msg.answer(f'@{msg.from_user.username}, использовать данную команду необходимо ответив на чье-то сообщение.')