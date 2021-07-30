from ...db_con.get_db_conn import get_connection

""" Получаем кол-во вложений у заявки """
async def get_attach_count(ask_id):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"SELECT COUNT(ID) FROM tg_db.req_attachs WHERE ask_id={ask_id}")
        response = cur.fetchone()

        return response["COUNT(ID)"]

""" Получаем вложения """
async def get_attachs(ask_id, sender, send):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"SELECT name, type FROM tg_db.req_attachs WHERE ask_id={ask_id} AND sender='{sender}' AND send='{send}'")
        response = cur.fetchall()

        return response

""" Изменяем статус вложениям """
async def edit_attach_status(ask_id, sender):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"UPDATE tg_db.req_attachs SET send='yes' WHERE ask_id={ask_id} AND sender='{sender}'")
        db.commit()