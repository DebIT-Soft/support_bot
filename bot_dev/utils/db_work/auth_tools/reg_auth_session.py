from ...db_con.get_db_conn import get_connection
from random import randint

from ...send_auth_code import build_body

# Регистрации сессии с авторизацией в базе
async def reg_session(webName, tgName, email):
    # Генерируем код
    code = randint(1000, 9999)

    # Отправляем сообщение
    build_body(email, webName, str(code))

    # Регистрируем в базе
    with get_connection() as db:
        cur = db.cursor()
        cur.execute(f"INSERT INTO tg_db.sessions (ID, auth_date, web_name, tg_name, sent_code, response) VALUES (NULL, CURRENT_TIMESTAMP, '{webName}', '{tgName}', {code}, 'отправлен')")
        db.commit()

    return code