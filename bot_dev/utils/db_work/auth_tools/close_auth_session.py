from ...db_con.get_db_conn import get_connection

""" Закрываем сессию """
async def close_session(user):
    try:
        with get_connection() as db:
            cur = db.cursor()
            cur.execute(f"UPDATE tg_db.sessions SET response='отменен' WHERE tg_name='{user}' AND response='отправлен'")
            db.commit()
    except:
        pass