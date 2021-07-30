import asyncio
from json import load
from os import dup
from typing import Union
from aiogram.types.callback_query import CallbackQuery

from aiogram.types.message import Message
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import USERS
from loader import dp
from keyboards.default.upanel import *
from aiogram.dispatcher.filters import Text
from utils.other.users_process import build_profile, dump_paid_products

from keyboards.inline.user_inline import *

""" Профиль """
@dp.message_handler(Text(equals='👤 Профиль'))
async def get_profile(msg: Message):
    await show_profile(msg = msg)

# Отправка юзеру профиля
async def show_profile(msg: Union[CallbackQuery, Message]):
    # Загружаем профиль и список продуктов
    profile_msg, prod_li = await build_profile(msg.from_user.username)

    # Загружаем клавиатуру
    markup = await profile_kb(prod_li)

    # Если прилетело сообщние, то отправляем профиль
    if isinstance(msg, Message):
        await msg.answer(profile_msg, reply_markup = markup)

    # Если прилетела CBQ
    if isinstance(msg, CallbackQuery):
        call = msg

        await call.message.edit_text(profile_msg, reply_markup = markup)

# Просмотр продуктов
async def show_my_product(call: CallbackQuery, product):
    # Загружаем клавиатуру
    markup = await products_kb()

    # Загружаем информацю о продукте
    prod_info = await dump_paid_products(product, call.from_user.username)

    # Изменяем сообщение
    await call.message.edit_text(prod_info, reply_markup = markup)

""" Обработка cb_data для просмотра продуктов """
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('prod'))
async def products_process(callback_query: types.CallbackQuery, state: FSMContext):
    # Выгружаем полученные callback_data в список
    cb_data = []
    for item in callback_query.data.split(":"):
        if not item.strip():
            continue
        cb_data.append(item.strip())
    
    # Нажата кнопка закрыть
    if cb_data[1] == 'close':
        await callback_query.message.delete()
    # Кнопка назад
    elif cb_data[1] == 'back':
        await show_profile(msg = callback_query)
    # Нажата кнопка выбора продукта
    else:
        await callback_query.answer('♻️ Загрузка...')
        await show_my_product(call = callback_query, product = cb_data[1])

""" Настройки """
@dp.message_handler(Text(equals='⚙️ Настройки'))
async def get_settings(msg: Message):
    await msg.answer('🔖 Скоро добавим :)')

""" Помощь """
@dp.message_handler(Text(equals='📜 Помощь'))
async def get_help(msg: Message):
    await msg.answer('Жми на кнопку, там все расписано!', reply_markup=await open_help_page())

""" Заявки """
@dp.message_handler(Text(equals='📬 Мои заявки'))
async def get_my_requests(msg: Message):
    await msg.answer('🔖 Скоро добавим :)')

""" Чат """
@dp.message_handler(Text(equals='💬 Наш чат'))
async def get_chat(msg: Message):
    await msg.answer('Чтобы присоединиться к нашему чату, жми сюда @DEBitChat')