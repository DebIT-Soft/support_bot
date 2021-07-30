from aiogram.dispatcher.filters.state import State, StatesGroup

""" Авторизация """
class Auth(StatesGroup):
    username = State()
    get_code = State()

""" Создание заявки """
class Request(StatesGroup):
    s = State()
    name = State()
    theme = State()
    err_code = State()
    msg = State()
    ask_id = State()
    have_attach = State()
    attach_type = State()

""" Ответ пользователя на заявку """
class uAnswer(StatesGroup):
    msg = State()
    attach_type = State()
    have_attach = State()
    ask_id = State()
    s = State()

""" Ответ оператора на ответ пользователя :) """
class AnswerToAnswer(StatesGroup):
    s = State()
    msg = State()
    ask_id = State()
    have_attach = State()
    attach_type = State()
    curr_support = State()
    user_id = State()

""" Стейты для клавиатур """
class kbState(StatesGroup):
    curr_kb = State()

""" Прием сообщения для рассылки """
class bCast(StatesGroup):
    sender = State()
    msg = State()
    from_chat = State()

""" Создание новой темы обращния """
class newTheme(StatesGroup):
    theme = State()
    emoji = State()
    emoji_old = State()

""" Стейт для клавиатуры взаимодействия с заявками """
class supportKB(StatesGroup):
    level = State()
    category = State()
    sub_category = State()
    ask = State()
    get_ans = State()
    msg = State()
    ask_id = State()
    have_attach = State()
    attach_type = State()
    curr_support = State()
    user_id = State()
    action = State()