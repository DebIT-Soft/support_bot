import asyncio
import logging
from os import stat

from aiogram.types.message import Message
from utils.other.users_process import is_subs
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.upanel import *
from keyboards.inline.user_inline import *
from states.all_states import Auth
from utils.db_work.auth_tools.check_user import get_email
from utils.db_work.auth_tools.reg_auth_session import reg_session
from utils.db_work.auth_tools.close_auth_session import close_session
from utils.db_work.auth_tools.save_auth_data import save_auth
from utils.db_work.users_tools.getting_user_info import get_user_info
from loader import dp

# region Авторизация
""" Отмена авторизации """
@dp.message_handler(Text(contains='Выйти'), state='*')
async def decline_auth(msg: Message, state: FSMContext):
    await msg.answer(
        'Авторизация отменена.',
        reply_markup=await upanel_kb()
    )

    # Если нажата кнопка отменить в момент ожидания кода
    if await state.get_state() == 'Auth:get_code':
        await close_session(msg.from_user.username)

    await state.finish()

""" Авторизация, ввод имени пользователя """
@dp.message_handler(Text(contains='Авторизоваться'))
async def authorization(msg: Message):
    # Обрабатываем сообщения только из лички
    if msg.chat.id > 0:
        await msg.answer(
            'Отправь мне имя пользователя, которое ты указывал при регистрации на нашем сайте.',
            reply_markup=await cancel_auth()
        )

        await Auth.username.set()

""" Отправка кода """
@dp.message_handler(state=Auth.username)
async def get_username(msg: Message, state: FSMContext):
    if len(msg.text) > 0:
        await msg.answer('Проверяю информацию...')

        # Проверяем пользователя
        response = await get_email(msg.text)

        if response is False:
            await msg.answer(f'Пользователь {msg.text} не найден. Попробуй еще раз...\n\nОтправь мне имя пользователя, которое ты указывал при регистрации на нашем сайте.')
        else:
            await msg.answer(
                f'На твою почту ({response}) отправлено письмо с кодом подтверждения, он действителен в течение <b>часа</b>, отправь его мне, чтобы завершить авторизацию :)\n\n' +
                f'<i>P.S.: Не забудь проверить папку \"Спам\", иногда письма попадают в нее.</i>'
            )

            code = await reg_session(msg.text, msg.from_user.username, response)

            async with state.proxy() as data:
                data['username'] = msg.text
                data['get_code'] = code

            await Auth.get_code.set()

""" Получение кода """

# Код указан не числом
@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Auth.get_code)
async def process_auth_code_e(msg: Message, state: FSMContext):
    await msg.answer('Код должен быть указан в виде числа.\nОтправь мне код.')

# Код указан числом
@dp.message_handler(lambda msg: msg.text.isdigit(), state=Auth.get_code)
async def process_auth_code(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        if data['get_code'] == int(msg.text):
            await msg.answer('Авторизация успешно пройдена!\n\nПожалуйста, подожди немного, я сохраняю твой профиль 🙂')

            subs_param, text = await is_subs(msg.from_user.id)

            if subs_param != 'ok':
                await msg.answer(
                        text,
                        reply_markup=await join_us(msg.from_user.id, subs_param)
                    )
            

            # Сохраняем данные
            await save_auth(msg.from_user.username, msg.text)

            # Сохраняем юзера
            await get_user_info(msg.from_user.username, msg.from_user.id, data['username'])

            await state.finish()
            await msg.answer(
                'Все готово, теперь я смогу полноценно тебе помогать :)\n' +
                'Для получения справки воспользуйся кнопкой <b>\"Помощь\"</b> или введи /help.\n\n',
                reply_markup=await upanel_kb()
                )
        else:
            await msg.answer('Неверный код, попробуй еще раз.')
# endregion


# region Пользователь без учетной записи
@dp.message_handler(Text(contains='У меня еще нет учетной записи'))
async def unauthorized(msg: Message):
    await msg.answer(
        'Очень жаль, ты можешь зарегистрироваться прямо сейчас! Для этого воспльзуйся кнокой ниже.\n\n' +
        'Также без авторизации ты можешь создать несколько заявок, но их приоритет, к сожалению, будет минимальный.',
        reply_markup=await register_kb()
    )
# endregion