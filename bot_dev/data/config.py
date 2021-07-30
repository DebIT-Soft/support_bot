from environs import Env

env = Env()
env.read_env()

import json

# Токен бота
BOT_TOKEN = env.str("BOT_TOKEN")

# Список админов и операторов
ADMINS = list(map(int, env.list("ADMINS")))
SUPPORTS = list(map(int, env.list("SUPPORTS")))

# Забаненные юзеры
BANNED_USERS = list(map(int, env.list("BLACK_LIST")))

# Наш чат и канал
OUR_CHAT = env.str("OUR_CHAT")
OUR_CHANNEL = env.str("OUR_CHANNEL")

# Саппорт-чат
SUPPORT_CHAT = env.str("SUPPORT_CHAT")

# IP
IP = env.str("ip")

# Режим отладки
DEBUG_MODE = True

# Словарь с пользователями
USERS = json.load(open('./users.json', encoding='utf-8-sig'))
# Словарь с темами
THEMES = json.load(open('./req_themes.json', encoding='utf-8-sig'))

# Список айдишек пользователей для рассылки
# USERS_ID = [721554927, 451568125, 417987918, 713132692, 252183627, 1060796670]

USERS_ID = [
    417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 
    417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 417987918, 
]

""" for user in USERS:
    USERS_ID.append(user['tg_id'])

print(USERS_ID) """