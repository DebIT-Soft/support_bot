from aiogram.types.message import ContentType, Message
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from data.config import SUPPORTS, SUPPORT_CHAT, OUR_CHAT
from aiogram.dispatcher.filters import Text
from aiogram import types
from loader import dp


@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(msg: Message):
    await dp.bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer(
        f'Привет, {msg.new_chat_members[0].first_name} 👋\n\n' +
        f'Вообще, изначально, я должен был только принимать заявки и отправлять уведомления, но ' + 
        'разрабы решили сделать из меня еще и чат-менеджера 🤖'
        )
    await dp.bot.send_sticker(msg.chat.id, r'CAACAgIAAx0CSG63EQADQmD4Gxb8y2w4WAan3bBSlDYShAo1AALYAQACVp29CpjUfylnzkA5IAQ')