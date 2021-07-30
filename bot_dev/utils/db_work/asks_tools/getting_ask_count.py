from ...db_con.get_db_conn import get_connection

""" Получаем кол-во заявок по категориям """
async def get_asks_count():
    with get_connection() as db:
        cur = db.cursor()
        cur.execute("SELECT COUNT(ask_id) FROM tg_db.requests WHERE theme='Проблемы с сайтом' AND status='открыт'")
        web_asks = cur.fetchone()
        
        cur.execute("SELECT COUNT(ask_id) FROM tg_db.requests WHERE theme='Проблемы с приложением' AND status='открыт'")
        app_asks = cur.fetchone()
        
        cur.execute("SELECT COUNT(ask_id) FROM tg_db.requests WHERE theme='Сотрудничество' AND status='открыт'")
        manage_asks = cur.fetchone()
        
        cur.execute("""SELECT COUNT(ask_id) FROM tg_db.requests WHERE theme != 'Проблемы с сайтом' AND 
        theme != 'Проблемы с приложением' AND theme != 'Сотрудничество' AND status='открыт'""")
        other_asks = cur.fetchone()
        
        asks_info = f'''Заявок в теме <b>Сайт</b>: <i>{web_asks["COUNT(ask_id)"]}</i>
        Заявок в теме <b>Приложение</b>: <i>{app_asks["COUNT(ask_id)"]}</i>
        Заявок в теме <b>Сотудничество</b>: <i>{manage_asks["COUNT(ask_id)"]}</i>
        Заявок в теме <b>Другое</b>: <i>{other_asks["COUNT(ask_id)"]}</i>\n
        Выберите категорию:'''.replace('        ', '')

        return asks_info