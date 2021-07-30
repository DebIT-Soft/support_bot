from utils.db_con.get_db_conn import get_connection

""" Сохраняем данные """
async def save_auth(username, code):
    with get_connection() as db:
        cur = db.cursor()

        # Завершаем сессию с кодом
        cur.execute(f"UPDATE tg_db.sessions SET response='ok' WHERE tg_name='{username}' AND sent_code={code} AND response='отправлен'")
        db.commit()

        # Сохраняем данные
        cur.execute(f"""INSERT INTO web_db.users_info (info_id, user_id, tg_name) VALUES (NULL, (SELECT user_id FROM web_db.users WHERE user_name = 
        (SELECT web_name FROM tg_db.sessions WHERE tg_name='{username}' AND sent_code={code} AND response='ok')), '{username}')""")
        
        db.commit()

