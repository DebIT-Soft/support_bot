from datetime import datetime
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from data.config import USERS

""" Клавиатура для перехода к регистрации """
async def register_kb():
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton('🌐 Зарегистрироваться', url='https://debitsoft.ru/signup'))
    return inline_kb

""" Клавиатура для перехода в чат и канал """
async def join_us(user_id, subs_param):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    # Если юзера нет в чате и канале
    if subs_param == 'both':
        inline_kb.add(InlineKeyboardButton('💬 Наш чат', url='https://t.me/debitchat'), 
        InlineKeyboardButton('📢 Наш канал', url='https://t.me/debitnews')).add(
            InlineKeyboardButton('✔️ Я подписался(-ась)', callback_data=f'subs')
        )
    
    # Если юзера нет в чате
    if subs_param == 'group':
        inline_kb.add(InlineKeyboardButton('💬 Наш чат', url='https://t.me/debitchat'), 
            InlineKeyboardButton('✔️ Я подписался(-ась)', callback_data=f'subs')
        )

    # Если юзера нет в канале
    if subs_param == 'channel':
        inline_kb.add(InlineKeyboardButton('📢 Наш канал', url='https://t.me/debitnews'),
            InlineKeyboardButton('✔️ Я подписался(-ась)', callback_data=f'subs')
        )
    
    return inline_kb

""" Клавиатура для продолжения общения по заявке """
async def continue_request_kb(ask_id, user_id):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(InlineKeyboardButton('📝 Ответить', callback_data=f'cont_ask:answer:{ask_id}:{user_id}:{datetime.now()}'), 
                    InlineKeyboardButton('🔒 Завершить', callback_data=f'cont_ask:close:{ask_id}:{user_id}:{datetime.now()}'))
    return inline_kb

""" Клавиатура для перехода на статью с помощью """
async def open_help_page():
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton('📋 Открыть статью', url='https://telegra.ph/Ispolzovanie-bota-DEBitSupport-bot-07-22'))
    return inline_kb

""" Коавиатура в профиле """
async def profile_kb(products):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(InlineKeyboardButton('♦️ Все продукты', callback_data=f'prod:all'), 
        InlineKeyboardButton('❌ Закрыть', callback_data=f'prod:close'))
    inline_kb.row()
    for product in products:
        inline_kb.insert(InlineKeyboardButton(f'🔸 {product}', callback_data=f'prod:{product}'))

    return inline_kb

""" Клавиатура для сообщений с продуктами """
async def products_kb():
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(InlineKeyboardButton('⬅️ Назад', callback_data=f'prod:back'), 
        InlineKeyboardButton('❌ Закрыть', callback_data=f'prod:close'))

    return inline_kb