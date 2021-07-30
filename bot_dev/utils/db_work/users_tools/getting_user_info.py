# -*- coding: utf-8 -*-
from ...db_con.get_db_conn import get_connection
from utils.other.serialize_users import serialize_user
import asyncio


async def get_user_info(user_name, user_id, web_name):
    with get_connection() as db:
        cur = db.cursor()

        # Получаем имя организации, которой владеет юзер
        cur.execute(f"""
        SELECT club_name FROM miner_db.clubs WHERE user_id = 
        (SELECT user_id FROM web_db.users WHERE user_name='{web_name}')
        """)
        club_response = cur.fetchone()

        club = club_response["club_name"]

        # Получаем список и информацию о купленных продуктах
        cur.execute(f"""
        SELECT product_id, pay_date, exp_date, state FROM web_db.products_users WHERE user_id = (
            SELECT user_id FROM web_db.users WHERE user_name='{web_name}'
        )
        """)
        products_response = cur.fetchall()

        prod_li = []
        # Получаем сроки действия лицензии на продукты
        for product in products_response:
            cur.execute(f"""
            SELECT product_name, cost, rate FROM web_db.products WHERE product_id={product['product_id']}
            """)
            row = cur.fetchone()
            exp_date = ''
            if product["exp_date"] is None:
                exp_date = 'нет'
            else:
                exp_date = product["exp_date"].strftime("%Y.%M.%d %H:%M")
            prod_li.append({
                'name': f'{row["product_name"]}',
                'payment': f'{row["cost"]}',
                'rate': f'{row["rate"]}' ,
                'pay_date': f'{product["pay_date"].strftime("%Y.%M.%d %H:%M")}',
                'exp_date': f'{exp_date}',
                'state': f'{product["state"]}'
            })

        await serialize_user(user_name, user_id, web_name, club, prod_li, 'да', 'да')

""" Запуск в отдельном потоке """
async def start_getting_info(user_name, user_id, web_name):
    print('Start')
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(get_user_info(user_name, user_id, web_name))
    loop.run_forever()