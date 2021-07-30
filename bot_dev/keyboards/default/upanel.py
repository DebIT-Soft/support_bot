from utils.other.load_themes import loading_themes
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

""" Клавиатура для пользователей """
async def upanel_kb():
    req_button = KeyboardButton("✍️ Создать заявку")
    prof_btn = KeyboardButton("👤 Профиль")
    sett_btn = KeyboardButton("⚙️ Настройки")
    help_btn = KeyboardButton("📜 Помощь")
    myreq_btn = KeyboardButton("📬 Мои заявки")
    chat_btn = KeyboardButton("💬 Наш чат")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(req_button, myreq_btn).add(prof_btn, help_btn).add(sett_btn, chat_btn)

    return kb

""" Авторизация """
async def auth_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔐 Авторизоваться")).add(KeyboardButton("⛔️ У меня еще нет учетной записи"))
    return kb

""" Отмена авторизации """
async def cancel_auth():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("❌ Выйти"))
    return kb

""" Отмена заявки """
async def cancel_req():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("❌ Отмена"))
    return kb

""" Темы обращения """
async def themes_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    themes = await loading_themes('kb')

    for theme in themes:
        kb.add(KeyboardButton(f'{theme["emoji"]} {theme["category_name"]}'))

    kb.add(KeyboardButton("❌ Отмена"))

    return kb