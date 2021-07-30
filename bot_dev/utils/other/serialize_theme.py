# -*- coding: utf-8 -*-
import asyncio
import json
from utils.db_work.asks_tools.save_new_theme import save_theme
from data import config

""" Сохранение тем для создания заявок """
async def serialize_theme(name, emoji):
    await save_theme(name, emoji)

    exch_dict = json.load(open('req_themes.json', encoding='utf-8-sig'))
    exch_dict.append({
            'visible_name': f'{emoji} {name}',
            'alias': f'{name}'
            })
    with open('req_themes.json', 'w', encoding='utf-8-sig') as fw:
        for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(exch_dict):
            fw.write(chunk)

    await reload_themes_list()

""" Перезагрузка списка """
async def reload_themes_list():
    config.THEMES = json.load(open('./req_themes.json', encoding='utf-8-sig'))