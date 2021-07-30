# -*- coding: utf-8 -*-
import asyncio
from data.config import USERS, USERS_ID
import json

""" Сохранение информации о пользователе в файл """
async def serialize_user(user_name, user_id, web_name, club, products_li, in_group, in_chat):
    exch_dict = json.load(open('users.json', encoding='utf-8-sig'))
    exch_dict.append({
            'user_name': f'{user_name}',
            'tg_id': user_id, 
            'web_name': f'{web_name}', 
            'club': f'{club}',
            'products': products_li,
            'in_group': f'{in_group}', 
            'in_channel': f'{in_chat}',
            })
    with open('users.json', 'w', encoding='utf-8-sig') as fw:
        for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(exch_dict):
            fw.write(chunk)

    await reload_users_dict()
    # json.dump(exch_dict, open('users.json', 'w', encoding='UTF-8'), indent=4, ensure_ascii=False)

""" Перезагрузка списка """
async def reload_users_dict():
    USERS = json.load(open('./users.json', encoding='utf-8-sig'))

    for user in USERS:
        USERS_ID.append(user['tg_id'])