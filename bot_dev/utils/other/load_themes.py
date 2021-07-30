from utils.db_con.get_db_conn import get_connection

""" Загрузка доступных тем """
async def loading_themes(query_from):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute("SELECT category_name, emoji FROM tg_db.req_categories")
        response = cur.fetchall()
        if query_from != 'kb':
            themes = 'Доступные темы:\n\n'

            for theme in response:
                themes += f'{theme["emoji"]} {theme["category_name"]} | {theme["category_name"]}\n'

            return themes
            
        elif query_from == 'kb':
            return response
