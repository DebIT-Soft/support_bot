from utils.db_con.get_db_conn import get_connection

async def ask_reset(ask_id):
    # Добавление оператора, отвечающего на заявку
    with get_connection() as db:
        cur = db.cursor()
        cur.execute(f"UPDATE tg_db.requests SET support_name = NULL, status = 'открыт' WHERE ask_id = {ask_id} ")
        db.commit()