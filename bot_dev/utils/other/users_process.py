from loader import dp
from data.config import OUR_CHANNEL, OUR_CHAT, USERS

""" Поиск в чате и канале """
async def is_subs(user_id):
    in_group = await dp.bot.get_chat_member(OUR_CHAT, user_id)
    in_channel = await dp.bot.get_chat_member(OUR_CHANNEL, user_id)
    subs_param = msg = None

    if in_group.status == 'left' and in_channel.status == 'left':
        subs_param = 'both'
        msg = '<i>P.S.: Не забудь подписаться на наш новостной канал, чтобы быть в курсе всех новостей и обновлений, а также присоединиться к нашему чату. Заявки от пользователей, находящихся в нашем чате и канале обрабатываются в приоритетном режиме.</i>'
    elif in_group.status != 'left' and in_channel.status != 'left':
        subs_param = 'ok'
    elif in_group.status != 'left' and in_channel.status == 'left':
        subs_param = 'channel'
        msg = '<i>Отлично! Теперь ты состоишь в нашем чате, осталось подписаться на наш канал :). Не забывай, что заявки от пользователей, находящихся в нашем чате и канале обрабатываются в приоритетном режиме.</i>'
    elif in_group.status == 'left' and in_channel.status != 'left':
        subs_param = 'group'
        msg = '<i>Отлично! Теперь ты подписан на наш канал, осталось присоединиться к нашему чату :). Не забывай, что заявки от пользователей, находящихся в нашем чате и канале обрабатываются в приоритетном режиме.</i>'

    return subs_param, msg

""" Формирование профиля """
async def build_profile(user_name):
    for user in USERS:
        if user["user_name"] == user_name:
            prod_li = []
            for product in user["products"]:
                prod_li.append(product["name"])
            
            profile = f'''
            👤 Имя пользователя: <u>{user["web_name"]}</u>
            ♻️ ID: <i>{user["tg_id"]}</i>
            ⚜️ Организация: <b>{user["club"]}</b>
            🔗 Приобретенные продукты:
            {", ".join(prod_li)}
            \nДля просмотра более подробной информации о своих продуктах - воспользуйся кнопками ниже :)
            '''
            return profile.replace('            ', ''), prod_li
    
    return 'К сожалению, мне не удалось найти тебя в списке пользователей.\nОтчет уже отправлен разработчикам.'

""" Выгрузка информации о приобретенных продуктах """
async def dump_paid_products(product_name, user_name):
    products_info = ''
    counter = 1
    separator = '\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖'

    for user in USERS:
        if user["user_name"] == user_name:
            for product in user["products"]:
                # Все продукты
                if product_name == 'all':
                    if counter == len(user["products"]):
                        separator = ''

                    products_info += f'''ℹ️ Информация о продукте <u>{product["name"]}</u>:\n
                    ♻️ Статус подписки: <i>{product["state"]}</i>
                    💸Последний платеж: <i>{product["pay_date"]}</i>
                    📅Действует до: <i>{product["exp_date"]}</i>
                    💰Цена: <b>{product["payment"]}</b> р.
                    📆Тарификация: <b>{product["rate"]}</b>{separator}
                    '''.replace('                    ', '')

                    counter += 1
                # Конкретный продукт
                else:
                    if product_name == product["name"]:
                        products_info += f'''ℹ️ Информация о продукте <u>{product["name"]}</u>:\n
                        ♻️ Статус подписки: <i>{product["state"]}</i>
                        💸Последний платеж: <i>{product["pay_date"]}</i>
                        📅Действует до: <i>{product["exp_date"]}</i>
                        💰Цена: <b>{product["payment"]}</b> р.
                        📆Тарификация: <b>{product["rate"]}</b>
                        '''.replace('                        ', '')

            return products_info