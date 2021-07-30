from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from keyboards.default.upanel import *
from utils.other.users_process import is_subs
from keyboards.inline.user_inline import *
from loader import dp


""" Проверка подписки """
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subs'))
async def check_subscribe(callback_query: CallbackQuery, state: FSMContext):    
    subs_param, text = await is_subs(callback_query.from_user.id)

    if subs_param != 'ok':
        if subs_param == 'both':
            await dp.bot.answer_callback_query(callback_query.id, show_alert=True, text='🤔 Не вижу тебя в чате и канале.')
        else:
            await dp.bot.edit_message_text(
                text,
                callback_query.from_user.id,
                callback_query.message.message_id,
                reply_markup=await join_us(callback_query.from_user.id, subs_param)
                )
    else:
        await dp.bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await dp.bot.send_message(
            callback_query.from_user.id,
            f'Добро пожаловать :)'
        )
        await dp.bot.send_sticker(callback_query.from_user.id, r'CAACAgIAAx0CTiPmWgACHEpg-VwJR70h5OqR8oKRmlcEtzaw1QACSAEAAladvQo3yp1m9yOJ4CAE')