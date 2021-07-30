import asyncio
from aiogram import executor
from loader import dp, parse_mongo
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands   
from threading import Thread


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)





if __name__ == '__main__':
    # Запуск потока с парсером монги
    mongo_thr = Thread(target=parse_mongo, args=(asyncio.get_event_loop(),))
    mongo_thr.start()
    
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
