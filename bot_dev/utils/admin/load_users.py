from data.config import USERS

async def load_users_info():
    u_info = ''
    in_group = in_channel = None
    for user in USERS:
        u_info += f'Информация о @{user["user_name"]}:\n➖➖➖➖➖\nИмя пользователя: {user["web_name"]}\nID: {user["tg_id"]}\nВ чате: {user["in_group"]}\nВ канале: {user["in_channel"]}\n\n'

    return len(USERS), u_info
