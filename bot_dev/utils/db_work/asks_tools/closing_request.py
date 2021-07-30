from ...db_con.get_db_conn import get_connection

""" Закрываем заявку """
async def close_request(ask_id, status):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"UPDATE tg_db.requests SET status='{status}', close_date=CURRENT_TIMESTAMP WHERE ask_id={ask_id}")
        db.commit()