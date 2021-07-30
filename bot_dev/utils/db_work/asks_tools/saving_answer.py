from ...db_con.get_db_conn import get_connection
import re


""" Сохраняем ответ """
async def save_answer(ask_id, attach, uname, sname, question, answer):
    with get_connection() as db:
        cur = db.cursor()

        if sname is None and answer is None:
            cur.execute(f"INSERT INTO tg_db.req_processing (ID, ask_id, user_name, support_name, question, answer, u_attach, s_attach) VALUES (NULL, {ask_id}, '{uname}', '{sname}', '{question}', NULL, '{attach}', NULL)")
        else:
            cur.execute(f"UPDATE tg_db.req_processing SET support_name='{sname}', answer='{answer}', s_attach='{attach}' WHERE ask_id={ask_id}")
        
        db.commit()
