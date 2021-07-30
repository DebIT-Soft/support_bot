from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

""" Клавиатура для подтверждения новой темы """
async def confirm_theme():
    inline_kb = InlineKeyboardMarkup(row_width=2)

    inline_kb.add(InlineKeyboardButton('👌 Верно', callback_data='theme:confirm'),
                InlineKeyboardButton('✍️ Изменить', callback_data='theme:edit')).add(InlineKeyboardButton('❌ Отмена', callback_data='theme:decline'))

    return inline_kb

""" Клавиатура для корректировки создаваемой темы """
async def edit_theme():
    inline_kb = InlineKeyboardMarkup(row_width=2)

    inline_kb.add(InlineKeyboardButton('🙂 Смайлик', callback_data='theme:emoji'), 
                InlineKeyboardButton('📝 Имя', callback_data='theme:name')).add(InlineKeyboardButton('❌ Отмена', callback_data='theme:back'))

    return inline_kb