from aiogram.dispatcher.storage import FSMContext
from states.all_states import newTheme
from data.config import THEMES
from filters.all_filters import IsAdmin
from aiogram.types.message import Message

from loader import dp
from keyboards.default.suppanel import *

from keyboards.inline.support_inline import *
from utils.admin.load_users import load_users_info
from utils.other.load_themes import loading_themes

""" Получить список пользователей и информацию о них """
@dp.message_handler(IsAdmin(True), commands='users')
async def get_users(msg: Message):
    users_count, users_info = await load_users_info()
    await msg.answer(f'Количество пользователей: <b>{users_count}</b>\n\n{users_info}')

@dp.message_handler(commands='themes')
async def get_themes(msg: Message):
    await msg.answer(await loading_themes('admin'))



# @dp.message_handler(commands='mongo_start')
# async def start_mongo(msg: Message):
#     loop = asyncio.get_event_loop()
#     loop.create_task(between_funcs())