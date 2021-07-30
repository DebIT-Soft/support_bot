from aiogram.types.message import Message
from attr import resolve_types
from data.config import SUPPORT_CHAT
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.upanel import *
from keyboards.inline.user_inline import *
from utils.db_work.auth_tools.is_user_authorized import is_authorized
from utils.other.users_process import is_subs
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(msg: Message):
    # Обрабатываем сообщения только из лички
    if msg.chat.id > 0:
        # Проверяем, авторизован ли пользователь
        response = await is_authorized(msg.from_user.username)

        if response is False:
            # Если пользователь не авторизован
            await msg.answer(
                f'Привет, {msg.from_user.full_name}!\n\n' +
                f'Для начала работы необходимо авторизоваться, воспользуйся кнопкой <b>\"Авторизоваться\"</b> :)',
                reply_markup=await auth_kb()
            )
        else:
            # Если пользователь авторизован
            await msg.answer(
                f'С возвращением, {response}!\n\n' +
                f'Я загрузил панель для удобства работы🙂\n'+
                f'Для получения справки воспользуйся кнопкой \"Помощь\" или введи /help.',
                reply_markup=await upanel_kb()
            )

            subs_param, text = await is_subs(msg.from_user.id)

            if subs_param != 'ok':
                await msg.answer(
                        text,
                        reply_markup=await join_us(msg.from_user.id, subs_param)
                    )