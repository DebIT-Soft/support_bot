
import json
from filters.all_filters import IsSupport
from aiogram.types.message import Message
from states.all_states import kbState, supportKB
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import ADMINS, SUPPORTS
from utils.db_work.asks_tools.getting_ask_count import get_asks_count

from loader import dp
from keyboards.default.suppanel import *
from aiogram.dispatcher.filters import Text

from keyboards.inline.support_inline import *

# 1. Загрузка панели для операторов
async def send_support_keyboard(msg: Message):
    await msg.answer(
        'Открываю панель для операторов...',
        reply_markup=await spanel_kb()
    )
    await supportKB.category.set()


# 2. Загрузка заявок в определнной категории
async def load_tg_requests(msg: Message):
    await msg.answer(
        'Загружаю информацию о заявках в ТГ...'
    )

    await msg.answer(
        f'Информация о заявках в <b>ТГ</b>:\n\n{await get_asks_count()}',
        reply_markup=await choose_cats()
    )


# 3. Загрузка заявок в определнной подкатегории
async def load_asks_in_category(msg: Message, state: FSMContext):
    await msg.answer('Загружаю открытые заявки...')

    THEMES = json.load(open('./req_themes.json', encoding='utf-8-sig'))
    u_theme = msg.text

    for theme in THEMES:
        if theme['visible_name'] == u_theme:
            u_theme = theme['alias']

    async with state.proxy() as data:
        data['category'] = u_theme

    await msg.answer(
        f'Список открытых заявок в категории <b>{data["category"]}</b>:',
        reply_markup = await open_requests(data['category'])
        )


# Кнопки назад - главная
@dp.message_handler(IsSupport(True), Text(contains='Назад'), state="*")
@dp.message_handler(IsSupport(True), Text(contains='Главная'), state="*")
async def returning(msg: Message, state: FSMContext):
    curr_state = await state.get_state()
    print(curr_state)

    if msg.text.__contains__('Главная'):
        await send_support_keyboard(msg = msg)

    
    elif msg.text.__contains__('Назад'):
        if curr_state == 'supportKB:category':
            await send_support_keyboard(msg = msg)
        
        elif curr_state == 'supportKB:sub_category':
            await send_support_keyboard(msg = msg)

        elif curr_state == 'supportKB:ask':
            await load_tg_requests(msg = msg)
            await supportKB.sub_category.set()
        
        elif curr_state == 'supportKB:get_ans':
            await msg.answer('Сначала необходимо дать ответ на заявку, либо отклонить ее (или же нажать закрыть)')


""" Открыть панель для операторов """
@dp.message_handler(IsSupport(True), commands='spanel')
async def open_spanel(msg: Message, state: FSMContext):
    await send_support_keyboard(msg = msg)

""" Получить список открытых заявок в ТГ """
@dp.message_handler(IsSupport(True), state=supportKB.category)
async def get_tg_requests(msg: Message):
    if msg.text.__contains__('Открытые заявки (ТГ)'):
        await load_tg_requests(msg = msg)
        await supportKB.sub_category.set()
    else:
        await msg.answer('В разработке...')

""" Обработка категорий """
@dp.message_handler(state=supportKB.sub_category)
async def get_category(msg: Message, state: FSMContext):
    await load_asks_in_category(msg = msg, state = state)
    await supportKB.ask.set()
