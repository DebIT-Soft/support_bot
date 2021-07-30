import asyncio
from aiogram.types.callback_query import CallbackQuery
from aiogram_broadcaster import TextBroadcaster

from aiogram.types.message import ContentType, Message
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import ADMINS, SUPPORTS, SUPPORT_CHAT, OUR_CHAT, USERS_ID
from aiogram.dispatcher.filters import Text
from aiogram import types
from states.all_states import bCast
from keyboards.inline.support_inline import start_bcast
from loader import dp
from time import time
from threading import Thread

""" Рассылка пользователям бота """
async def bcast_sending(message):
    start_t = time()
    await TextBroadcaster(USERS_ID, message).run()
    await dp.bot.send_message(SUPPORT_CHAT, f'Рассылка завершена, затрачено {time() - start_t} с.')

@dp.message_handler(commands='broadcast')
async def start_broadcasting(msg: Message, state: FSMContext):
    if msg.from_user.id in SUPPORTS or msg.from_user.id in ADMINS:
        await msg.answer(
            f'@{msg.from_user.username}, отправь мне текст рассылки.\n\n' +
            f'<i>P.S.: Для форматирования текста воспользуйся html-тегами, пока что ' +
            f'я умею обрабатывать только их :)</i>'
        )
        await bCast.sender.set()

        async with state.proxy() as data:
            data['sender'] = msg.from_user.username

        await bCast.msg.set()

@dp.message_handler(state=bCast.msg)
async def get_bcast_msg(msg: Message, state: FSMContext):
    sender = None
    async with state.proxy() as data:
        sender = data['sender']
        data['msg'] = msg.text
        data['from_chat'] = msg.chat.id
    if sender == msg.from_user.username:
        await msg.answer(f'Текст рассылки:\n\n{data["msg"]}\n\nВсе верно?', reply_markup=await start_bcast())

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bcast'), state="*")
async def processing_bcast(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in SUPPORTS or callback_query.from_user.id in ADMINS:
        async with state.proxy() as data:
            bcast_chat = data['from_chat']
        if callback_query.data == 'bcast:start':
            await dp.bot.send_message(bcast_chat, f'Рассылка успешно запущена :). Получателей: {len(USERS_ID)}')
            await dp.bot.delete_message(bcast_chat, callback_query.message.message_id)
            
            async with state.proxy() as data:
                bcast_msg = data['msg'] + '\n\nТы получил данное сообщение, потому что находишься в списке тестировщиков.'
            await state.finish()
            
            # Запускаем в отдельном потоке
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(bcast_sending(bcast_msg))
            loop.run_forever()
        else:
            await dp.bot.send_message(bcast_chat,
                f'@{callback_query.from_user.username}, отправь мне текст рассылки.\n\n' +
                f'<i>P.S.: Для форматирования текста воспользуйся html-тегами, пока что ' +
                f'я умею обрабатывать только их :)</i>'
            )
            await dp.bot.delete_message(bcast_chat, callback_query.message.message_id)