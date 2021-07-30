import datetime
from ...db_con.get_db_conn import get_connection

""" Получаем информацию о заявке """
async def get_ask_info(ask_id):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"SELECT open_date, tg_name, tg_id, web_name, theme, err_code, msg, attach, type FROM tg_db.requests WHERE ask_id={ask_id}")
        response = cur.fetchone()


        ask_info = f'''Информация о заявке #{ask_id} от @{response["tg_name"]}:\n
        Создана: <b>{response["open_date"].strftime("%d.%m.%Y %H:%M")}</b>
        Имя пользователя: <b>{response["web_name"]}</b>
        Тема: <b>{response["theme"]}</b>
        Код ошибки: <b>{response["err_code"]}</b>
        Вложения: <b>{response["attach"]}</b>
        Тип вложений: <b>{response["type"]}</b>
        Сообщение: \n
        {response["msg"]}\n
        Для взаимодействия воспользуйтесь кнопками ниже.
        ⚠️ <b>Важно! Если не можете дать ответ - нажмите кнопку Закрыть.</b>'''.replace('        ', '')

        return ask_info, response["tg_id"]