from ...db_con.get_db_conn import get_connection
import re


# Проверяем почту
async def get_email(username):
    with get_connection() as db:
        cur = db.cursor()
        # Делаем запрос в таблицу uInfo базы webDB
        cur.execute(f"SELECT email FROM web_db.users WHERE user_name='{username}'")
        # И пробуем получить ID пользователя, к которому привязан этот ТГ
        email = cur.fetchone()
        typeOf = type(email)
        # Если база вернула NoneType-объект, значит, пользователя нет в базе
        if re.search('NoneType', str(typeOf)):
            return False
        else:
            # Иначе - пользователь есть, берем его мыло
            return email['email']