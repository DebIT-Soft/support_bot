import re
from ...db_con.get_db_conn import get_connection

""" Проверяем, привязан ли этот ТГ к какой-нибудь учетке """
async def is_authorized(username):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"SELECT user_name FROM web_db.users WHERE user_id = (SELECT user_id FROM web_db.users_info WHERE tg_name = '{username}')")
        response = cur.fetchone()
        if re.search('None', str(type(response))):
            return False
        else:
            return response['user_name']