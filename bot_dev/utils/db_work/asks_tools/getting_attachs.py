from ...db_con.get_db_conn import get_connection

async def get_attach_files(ask_id, sender):
    with get_connection() as db:
        cur = db.cursor()
        cur.execute(f"SELECT name, type FROM tg_db.req_attachs WHERE ask_id={ask_id} AND sender='{sender}' AND send='no'")
        files = cur.fetchall()

        return files