import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

""" 
Парсер монги расположен имеено здесь,
чтобы избежать повторной инициализации бота
в отдельном модуле
"""
def parse_mongo(loop):
    from utils.db_con.get_mongo_conn import get_mconn
    asyncio.set_event_loop(loop)
    
    with get_mconn() as db:
        coll = db.app_info

        # Обрабатывать будем все данные, которые поступили
        # через операцию insert
        parser = coll.watch([{
            '$match': {
                'operationType': {
                    '$in': ['insert']
                }
            }
        }])

        for change in parser:
            msg_text = None
            admins_msg = None

            # Для упрощения обращения к изменениям в базе
            data = change["fullDocument"]

            # Обрабатываем данные только в том случае, если они
            # адресованы боту
            if data["to"] == 'Bot':
                if data["type"] == 'crash':
                    msg_text = f'''🤕 Упс... Кажется, что-то сломалось.

                    Привет, хочу сообщить тебе о том, что на компьютере
                    <b>{data['pc_name']}</b> не удалось запустить майнер,
                    лог уже отправлен разработчикам, давай создадим заявку в поддержку :)
                    '''

                    admins_msg = f'''🤕 Упс... Кажется, что-то сломалось.

                    Вечер в хату, по-видимому, майнер не захотел запускаться. Подробности:
                    Организация: <b>{data['club']}</b>
                    Компьютер: <b>{data['pc_name']}</b>
                    Конфигурация ПК:
                    ➖➖➖➖➖➖➖➖➖➖➖➖
                    <b>ОС:</b> {data['os']}
                    <b>Версия:</b> {data['os_ver']}
                    <b>Процессор:</b> {data['cpu']}
                    <b>Объем ОП:</b> {data['ram']}
                    <b>Видеокарта:</b> {data['video_card']}
                    '''
                
                if data["type"] == 'notify':
                    if data["sub_type"] == 'lic_exp':
                        msg_text = f'''🕑 Истек срок действия лицензии.

                        Привет, хочу сообщить тебе о том, что у тебя закончился срок действия
                        лицензии на продукт <b>{data['app_name']}</b>.
                        
                        <i>Для продления воспользуйся кнопкой ниже :)</i>
                        '''.replace('    ', '')

                if data["type"] == 'error':
                    msg_text = f'''
                    🤕 Упс... Кажется, что-то сломалось.

                    Привет, хочу сообщить тебе о том, что на компьютере
                    <b>{data['pc_name']}</b> произошла ошибка. Подробности:
                    Продукт: <b>{data['app']}</b>
                    Код ошибки: <b>{data['err_code']}</b>

                    <i>Думаю, стоит перезагрузить компьютер, если ошибка не пропадет, то
                    можем открыть заявку в поддержку :)</i>
                    '''

                    admins_msg = f'''🤕 Упс... Кажется, что-то сломалось.

                    Вечер в хату, в продукте <b>{data['app']}</b> произошла ошибка <i>({data['err_code']})</i>.
                    '''
                
                asyncio.run_coroutine_threadsafe(
                    send_data(
                        data["user_id"], 
                        msg_text.replace('                    ', ''), 
                        admins_msg.replace('                    ', '')), 
                        loop=loop)                
                # loop.create_task(send_data(data["user_id"], data["msg"]))

async def send_data(user_id, msg, admins_msg):
    await bot.send_message(
        user_id, msg
    )

    if admins_msg is not None:
        await bot.send_message(
            config.SUPPORT_CHAT,
            admins_msg
        )