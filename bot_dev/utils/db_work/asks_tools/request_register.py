import re
from ...db_con.get_db_conn import get_connection

""" Регистрация заявки """
async def request_reg(time, ask_id, uname, uid, web_uname, theme, err_code, msg, have_attach, attach_type):
    with get_connection() as db:
        cur = db.cursor()

        # Временная регистрация
        if time == 'first':
            cur.execute(f"INSERT INTO tg_db.requests (ask_id, open_date, tg_name, tg_id, web_name, theme, err_code, msg, attach, type, answer, support_name, status, close_date, ask_proc, proc_name) VALUES (NULL, CURRENT_TIMESTAMP, '{uname}', {uid}, '{web_uname}', '{theme}', {err_code}, 'process', 'process', 'process', NULL, NULL, 'открыт', NULL, NULL, NULL)")
            db.commit()

            cur.execute("SELECT LAST_INSERT_ID() FROM tg_db.requests")
            response = cur.fetchone()

            return response['LAST_INSERT_ID()']

        # Сохранение заявки в базе
        if time == 'finish':
            cur.execute(f"UPDATE tg_db.requests SET msg='{msg}', attach='{have_attach}', type='{attach_type}' WHERE ask_id={ask_id} AND tg_name='{uname}' AND status='открыт' AND msg='process' AND attach='process' AND type='process'")
            db.commit()