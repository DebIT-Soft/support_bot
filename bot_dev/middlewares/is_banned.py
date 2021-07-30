from aiogram.dispatcher.handler import CancelHandler
from aiogram.types.update import Update
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import dp

from data.config import BANNED_USERS

class IsBanned(BaseMiddleware):
    """ 
    Проверка, находится ли юзер в ЧС
    """

    async def on_pre_process_update(self, upd: Update, data: dict):
        if upd.message:
            user = upd.message.from_user.id
        elif upd.callback_query:
            user = upd.callback_query.from_user.id
        else:
            return
        
        if user in BANNED_USERS:
            await dp.bot.send_message(user, 'Ты в черном списке.')

            raise CancelHandler()
