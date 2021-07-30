from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

from utils.db_work.asks_tools.getting_asks import get_asks, load_asks_cat

""" Клавиатура для операторов """
async def spanel_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('📬 Открытые заявки (ТГ)')).add(KeyboardButton('📧 Открытые заявки (сайт)')).add(KeyboardButton('♻️ Обновить зависшие заявки'))
    return kb

""" Клавиатура для выбора категорий """
async def choose_cats():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    reg_cats, unreg_cats = await load_asks_cat()

    for reg_cat in reg_cats:
        kb.add(KeyboardButton(f'{reg_cat["emoji"]} {reg_cat["category_name"]}'))

    if len(unreg_cats) > 0:
        kb.add(KeyboardButton('🏷 Категория Другое'))

    kb.add(KeyboardButton('🔙 Назад'))

    return kb

""" Загрузка заявок в клавиатуру под определенную категорию """
async def open_requests(category):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    kb.add(KeyboardButton('🔙 Назад'), KeyboardButton('⭕️ Главная'))
    kb.row()
    # Получаем открытые заявки
    open_asks = await get_asks(category)

    for ask in open_asks:
        kb.insert(KeyboardButton(f'✉️ Заявка #{ask["ask_id"]}'))

    return kb