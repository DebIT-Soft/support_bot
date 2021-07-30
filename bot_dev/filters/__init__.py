from aiogram import Dispatcher

from loader import dp
from .all_filters import IsAdmin, IsSupport


if __name__ == "filters":
    print('Филтры загружены')
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsSupport)
    pass
