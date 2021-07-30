from utils.db_con.get_db_conn import get_connection

""" Закрепляем заявку за оператором """
async def pin_ask(support, ask_id):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"UPDATE tg_db.requests SET support_name='{support}', status='ожидание' WHERE ask_id={ask_id}")
        db.commit()