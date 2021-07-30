import re
from ...db_con.get_db_conn import get_connection

""" Отмена заявки пользователем """
async def decl_request(ask_id):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"UPDATE tg_db.requests SET status='отменен' WHERE ask_id={ask_id}")
        db.commit()