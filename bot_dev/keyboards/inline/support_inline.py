from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from utils.db_work.asks_tools.processing_attachs import get_attach_count


""" Клавиатура для работы с заявкой """
async def work_with_request(ask_id, user_id):
    # Получем кол-во вложений у заявки
    attach_count = await get_attach_count(ask_id)
    btn_answ = InlineKeyboardButton('📝 Ответить', callback_data=f'req_proc:answer:{ask_id}:{user_id}')
    btn_decl = InlineKeyboardButton('🗑 Отклонить', callback_data=f'req_proc:cancel:{ask_id}:{user_id}')
    btn_close = InlineKeyboardButton('❌ Закрыть', callback_data=f'req_proc:close:{ask_id}:{user_id}:{attach_count}')

    inline_kb = InlineKeyboardMarkup(row_width=2).add(btn_answ, btn_decl).add(btn_close)

    return inline_kb

""" Клавиатура для работы с ответом на заявку """
async def work_with_user_answer(ask_id, user_id):
    # Получем кол-во вложений у ответа
    attach_count = await get_attach_count(ask_id)
    btn_answ = InlineKeyboardButton('📝 Ответить', callback_data=f'scont_ask:answer:{ask_id}:{user_id}')
    btn_close = InlineKeyboardButton('❌ Закрыть', callback_data=f'scont_ask:close:{ask_id}:{user_id}')

    inline_kb = InlineKeyboardMarkup(row_width=2).add(btn_answ, btn_close)

    return inline_kb

""" Клавиатура для подтверждения рассылки """
async def start_bcast():
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton('👌 Да', callback_data='bcast:start'), InlineKeyboardButton('✍️ Изменить', callback_data='bcast:edit'))

    return inline_kb