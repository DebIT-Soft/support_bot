from utils.db_con.get_db_conn import get_connection

""" Сохранение новой темы в базе """
async def save_theme(theme_name, emoji):
    with get_connection() as db:
        cur = db.cursor()

        cur.execute(f"INSERT INTO tg_db.req_categories (ID, category_name, emoji) VALUES (NULL, '{theme_name}', '{emoji}')")

        db.commit()