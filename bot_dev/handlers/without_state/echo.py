from handlers.supports.spanel import send_support_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import SUPPORTS, SUPPORT_CHAT, DEBUG_MODE, USERS
from keyboards.default.suppanel import spanel_kb
from keyboards.default.upanel import upanel_kb

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(msg: types.Message):
    if DEBUG_MODE is True:
        if msg.from_user.id in SUPPORTS:
            await msg.answer('🚫 Сессия истекла.')

            await send_support_keyboard(msg = msg)
        else:
            await msg.answer('🚫 Неизвестная команда.', reply_markup=await upanel_kb())
        # await msg.answer(f'Сообщение без стейта.\n\n{msg}')
        # await msg.answer('Сообщение без стейта, работаем над этим :)')

# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(msg: types.Message, state: FSMContext):
    if msg.chat.id > 0:
        state = await state.get_state()
        await msg.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                            f"\nСодержание сообщения:\n"
                            f"<code>{msg}</code>")
    # await msg.answer_sticker(r'CAACAgIAAxkBAAIIp2D16Qw3GiNEaDe9EVy5IFIiCjuDAAJGAQACVp29CkdInwU0JztkIAQ')

