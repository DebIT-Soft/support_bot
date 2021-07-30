from data.config import ADMINS, SUPPORTS, BANNED_USERS
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message


class IsAdmin(BoundFilter):
    """ 
    Фильтр для проверки, является
    ли юзер админом
    """

    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, msg: Message):
        if (msg.from_user.id in ADMINS) is False:
            await msg.answer(f'@{msg.from_user.username}, данная команда доступна только администраторам.')
        
        return msg.from_user.id in ADMINS

class IsSupport(BoundFilter):
    """ 
    Фильтр для проверки, является
    ли юзер оператором
    """

    key = 'is_support'

    def __init__(self, is_support):
        self.is_support = is_support

    async def check(self, msg: Message):
        if (msg.from_user.id in SUPPORTS) is False:
            await msg.answer(f'@{msg.from_user.username}, данная команда доступна только операторам.')
        
        return msg.from_user.id in SUPPORTS