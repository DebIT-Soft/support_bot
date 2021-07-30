import json
# from utils.users_process import user_proc
import asyncio
import sys
from utils.db_con.get_db_conn import get_connection
from utils.other.serialize_users import serialize_user
import datetime
import re
from utils.db_work.users_tools.getting_user_info import start_getting_info
import time

""" asyncio.run(start_getting_info('zzDust', 432123, 'itzDuster'))
while True:
    print('write') """

""" with get_connection() as db:
    cur = db.cursor()

    cur.execute("SELECT ExpDate, PayDate FROM webDB.products_users WHERE UserID=1 AND ProductID=2")
    rr = cur.fetchone()
    p = rr["PayDate"]
    e = rr["ExpDate"]

    # abc = str(e - datetime.datetime.today())
    abc = str(datetime.datetime(2021, 7, 23, 10, 22) - datetime.datetime(2021, 9, 23, 9, 21))
    time_li = []
    time_li_2 = []
    remain_time = None

    if re.search('day', abc):
        time_li = abc.split(",")
        if re.search('days', time_li[0]):
            time_li[0] = time_li[0].replace('days', 'д.')

        if re.search('day', time_li[0]):
            time_li[0] = time_li[0].replace('day', 'д.')

        remain_time = time_li[0]

        if re.search(' 00:00', time_li[1]):
            print(remain_time)
        else:
            time_li_2 = time_li[1].split(":")
            remain_time += f'{time_li_2[0]} ч. {time_li_2[1]} мин.'
            
    else:
        time_li = abc.split(":")
        remain_time = f'{time_li[0]} ч. {time_li[1]} мин.'
        if remain_time == '0 ч. 00 мин.':
            remain_time = 'Истекла'
        
    
    print(remain_time) """
    # if re.search('days', )
"""     days = abc.days
    if days > 0:
        days = f'{days} д.'
    hours = abc.hours
    if hours > 0:
        hours = f'{hours} ч.'
    mins = abc.minutes
    if mins > 0:
        mins = f'{mins} мин.'
    print(f'{days} {hours} {mins}') """

    # user_name = 'zzDust'
    # user_id = 417987918
    # web_name = 'itzDuster'
    
    # cur.execute(f"""SELECT ClubName FROM test.Clubs WHERE UserID=
    # (SELECT uID FROM webDB.Users WHERE uName='{web_name}')""")
    # club_resp = cur.fetchone()

    # club = club_resp['ClubName']

    # prod_li = []
    
    # cur.execute(f"""SELECT * FROM webDB.products_users WHERE UserID=
    # (SELECT uID FROM webDB.Users WHERE uName='{web_name}')""")
    # response = cur.fetchall()
    
    # for product in response:
    #     cur.execute(f"SELECT * FROM webDB.Products WHERE ProductID={product['ProductID']}")
    #     prod_info = cur.fetchone()
    #     prod_li.append({
    #         'name': f'{prod_info["Name"]}',
    #         'description': f'{prod_info["Description"]}',
    #         'payment': f'{prod_info["Price"]}',
    #         'rate': f'{prod_info["Rate"]}',
    #         'state': f'{prod_info["ProdStatus"]}',
    #         'time_remain': f'{prod_info["ExpDate"] - prod_info["PayDate"]}'
    #         })

    # asyncio.run(serialize_user(user_name, user_id, web_name, club, prod_li, 'да', 'да'))

""" 


products_li = []
response = [{'product_name': 'DEBit Miner', 'finish_date': '10.09.2021'}, {'product_name': 'DEBit Bot', 'finish_date': '19.10.2021'}, {'product_name': 'Some product', 'finish_date': '11.11.2021'}]
for product in response:
    products_li.append({'name': f'{product["product_name"]}', 'lic_exp': f'{product["finish_date"]}'})

asyncio.run(serialize_user('test_user', 1234567, 'mega_user', 'mega_club', products_li, 'yes', 'yes')) """


# print(sys.version_info[0])
# asyncio.run(user_proc('zzDust', 'is_authorized'))

""" users_dict = {
    'users': [
        { 'zzDust': {
            'tg_id': 417987918,
            'web_name': 'itzDuster',
            'in_group': 'yes',
            'in_channel': 'yes'
        },
        'debit_create': {
            'tg_id': 451568125,
            'web_name': 'dannebey',
            'in_group': 'yes',
            'in_channel': 'yes'
        } }
    ]
}

users_dict1 = {
    'zzDust': {
            'tg_id': 417987918,
            'web_name': 'itzDuster',
            'in_group': 'yes',
            'in_channel': 'yes'
        },
        'debit_create': {
            'tg_id': 451568125,
            'web_name': 'dannebey',
            'in_group': 'yes',
            'in_channel': 'yes'
        } 
}

test_dict = json.load(open('users.json'))
test_dict.update({'user1': {'tg_id': 12345, 'web_name': 'user12', 'in_group': 'yes', 'in_channel': 'no'}})
json.dump(test_dict, open('users.json', 'w'), indent=4) """



""" with open('users.json', 'w') as users_file:
    json.dump(users_dict, users_file, indent=4)

with open('users.json', 'r') as users_file:
    upd_dict = json.load(users_file)

print(upd_dict) """

""" abc = open('users.json', 'r')
gg = json.load(abc)
abc.close()
print(gg)

users = open('users.json', 'a')
json.dump(users_dict, users)
users.close()

print(f'Словарь users: {users_dict}\n')
for user_name, user_info in users_dict.items():
    if user_name == 'debit_create':
        print(f'Информация о debit_create: {users_dict.get("debit_create")}')
    
    if user_name == 'zzDust':
        print(f'Информация о zzDust: {users_dict.get("zzDust")}')

    print(f'\nИмя пользователя: {user_name}')
    print(f'\tТГ ID: {user_info["tg_id"]}')
    print(f'\tИмя пользователя (сайт): {user_info["web_name"]}')
    print(f'\tВ чате | В канале: {user_info["in_group"]} | {user_info["in_channel"]}\n')
 """