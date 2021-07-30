from ...db_con.get_db_conn import get_connection
import re


""" Сохраняем вложения """
async def save_attach(ask_id, attach, attach_type, sender, send):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"INSERT INTO tg_db.req_attachs (ID, ask_id, name, type, sender, send) VALUES (NULL, {ask_id}, '{attach}', '{attach_type}', '{sender}', '{send}')")
        db.commit()
