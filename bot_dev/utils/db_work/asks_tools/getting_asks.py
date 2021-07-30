from ...db_con.get_db_conn import get_connection

""" Выгружаем заявки определенной категории """
async def get_asks(category):
    with get_connection() as db:
        cur = db.cursor()

        if category == 'Другое':
            cur.execute("SELECT ask_id FROM tg_db.requests WHERE theme != 'Проблемы с сайтом' AND theme != 'Проблемы с приложением' AND theme != 'Сотрудничество' AND status='открыт'")
            response = cur.fetchall()
        else:
            cur.execute(f"SELECT ask_id FROM tg_db.requests WHERE theme='{category}' AND status='открыт'")
            response = cur.fetchall()

        return response

""" Выгрузка заявок по категориям """
async def load_asks_cat():
    with get_connection() as db:
        cur = db.cursor()

        # Получаем заявки по зарегистрированным категориям
        cur.execute('SELECT category_name, emoji from tg_db.req_categories')

        reg_categories = cur.fetchall()

        # Получем заявки по незарегистрированным категориям
        cur.execute('''SELECT theme FROM tg_db.requests WHERE theme NOT IN
        (SELECT category_name FROM tg_db.req_categories)
        ''')

        unreg_categories = cur.fetchall()

        return reg_categories, unreg_categories