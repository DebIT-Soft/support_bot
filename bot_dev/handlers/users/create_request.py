import json
import os
from utils.other.users_process import is_subs

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import ContentType, Message
from data.config import SUPPORT_CHAT
from keyboards.default.upanel import *
from keyboards.inline.user_inline import *
from loader import dp
from states.all_states import Request
from utils.db_work.asks_tools.decline_request import decl_request
from utils.db_work.auth_tools.is_user_authorized import is_authorized
from utils.db_work.asks_tools.request_register import request_reg
from utils.db_work.asks_tools.saving_attachs import save_attach

""" Отмена Заявки """
@dp.message_handler(Text(contains='Отмена'), state='*')
async def decline_auth(msg: Message, state: FSMContext):
    await msg.answer(
        'Заявка отменена.',
        reply_markup=await upanel_kb()
    )
    
    # Если нажата кнопка отменить в момент ввода кода ошибки или текста обращения
    curr_state = await state.get_state()
    if curr_state == 'Request:err_code':
        async with state.proxy() as data:
            theme = data['theme']
        if theme == 'Сотрудничество':
            async with state.proxy() as fata:
                ask_id = data['ask_id']
            await decl_request(ask_id)

    await state.finish()


""" Создание заявки """
@dp.message_handler(Text(equals="✍️ Создать заявку"), state="*")
async def create_req(msg: Message, state: FSMContext):
    # Обрабатываем сообщения только из лички
    if msg.chat.id > 0:
        # Проверяем, зарегистрирован ли пользователь
        uName = await is_authorized(msg.from_user.username)
        if uName is False:
            # Если пользователь не авторизован
            await msg.answer(
                f'Привет, {msg.from_user.full_name}!\n\n' +
                f'Для начала работы необходимо авторизоваться, воспользуйся кнопкой <b>\"Авторизоваться\"</b> :)',
                reply_markup=await auth_kb()
            )
        else:
            subs_param, subs_msg = await is_subs(msg.from_user.id)

            if subs_param != 'ok':
                await msg.answer(
                        subs_msg,
                        reply_markup=await join_us(msg.from_user.id, subs_param)
                    )
            # Если пользователь авторизован
            await msg.answer(
                'Введи тему обращения или выбери из списка:',
                reply_markup=await themes_kb()
            )

            # Записываем имя пользователя
            await Request.name.set()
            async with state.proxy() as data:
                data['name'] = uName

            await Request.theme.set()

""" Ввод темы обращения """
@dp.message_handler(state=Request.theme)
async def get_theme(msg: Message, state: FSMContext):
    THEMES = json.load(open('./req_themes.json', encoding='utf-8-sig'))

    u_theme = msg.text

    for theme in THEMES:
        if theme['visible_name'] == u_theme:
            u_theme = theme['alias']
    
    async with state.proxy() as data:
        data['theme'] = u_theme
    
    # Если выбрано сотрудничество
    if u_theme == 'Сотрудничество':
        await msg.answer(
            'Опиши свое предложение, если к сообщению будут прикреплены картинки или документы, ' +
            'то сначала отправь мне вложения, а потом само предложение. Если же ничего прикрепляться не будет, ' +
            'то просто отправь мне сообщение :).\n\n' +
            '<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>',
            reply_markup=await cancel_req()
        )

        # Временно регистрируем заявку
        ask_id = await request_reg('first', '-', msg.from_user.username, msg.from_user.id, data['name'], data['theme'], 0, '-', '-', '-')

        async with state.proxy() as data:
            data['err_code'] = 0
            data['ask_id'] = ask_id
            data['attach_type'] = None        

        await Request.msg.set()
    else:
        await msg.answer(
            'Введи код ошибки:',
            reply_markup=await cancel_req()
        )

        await Request.err_code.set()

""" Ввод кода ошибки """
@dp.message_handler(lambda msg: not msg.text.isdigit(), state=Request.err_code)
async def get_err_code_ex(msg: Message, state: FSMContext):
    await msg.answer(
        'Код должен быть указан в виде числа, попробуй еще раз.\n\nВведи код ошибки:',
        reply_markup=await cancel_req()
    )

@dp.message_handler(lambda msg: msg.text.isdigit(), state=Request.err_code)
async def get_err_code(msg: Message, state: FSMContext):
    await msg.answer(
        'Введи текст обращения, если к заявке будут прикреплены картинки или документы, то сначала отправь мне вложения, а потом текст обращения.\n\n'+
        '<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>',
        reply_markup=await cancel_req()
    )

    async with state.proxy() as data:
        data['err_code'] = msg.text
    
    # Временно регистрируем заявку и получаем ее ID
    ask_id = await request_reg('first', '-', msg.from_user.username, msg.from_user.id, data['name'], data['theme'], data['err_code'], '-', '-', '-')

    async with state.proxy() as data:
        data['ask_id'] = ask_id
        data['attach_type'] = None
    
    await Request.msg.set()

""" Ввод текста обращения """
@dp.message_handler(state=Request.msg, content_types=ContentType.PHOTO)
@dp.message_handler(state=Request.msg, content_types=ContentType.TEXT)
@dp.message_handler(state=Request.msg, content_types=ContentType.DOCUMENT)
async def get_message(msg: Message, state: FSMContext):
    # Костыль
    async with state.proxy() as data:
        data['s'] = 's'

    # Если отправлен документ
    if msg.content_type == 'document':
        # Если была попытка прикрепить документ к картинкам
        if data['attach_type'] == 'Картинка' and data['attach_type'] is not None:
            await msg.answer('🤕 Ошибка, к сообщению можно прикрепить либо картинки, либо документы.')
        else:
            async with state.proxy() as data:
                data['attach_type'] = 'Документ'

            # Получаем файл
            doc_info = await dp.bot.get_file(msg.document.file_id)
            # Разделяем полученный файл на имя и расширение
            doc_name, doc_extension = os.path.splitext(doc_info.file_path)
            # Скачиваем файл
            download_doc = await dp.bot.download_file(doc_info.file_path)
            # Указываем путь и имя файл
            # Храним файлы с UID в имени
            doc_src = 'documents/' + doc_info.file_unique_id + doc_extension
            # Сохраняем в базе
            await save_attach(data['ask_id'], doc_info.file_unique_id + doc_extension, 'Документ', 'user', 'no')
            
            # Сохраняем в каталог
            with open(doc_src, 'wb') as new_doc:
                new_doc.write(download_doc.getvalue())

    # Если отправлена картинка
    if msg.content_type == 'photo':
        # Если была попытка прикрепить картинку к документам
        if data['attach_type'] == 'Документ' and data['attach_type'] is not None:
            await msg.answer('🤕 Ошибка, к сообщению можно прикрепить либо картинки, либо документы.')
        else:
            async with state.proxy() as data:
                data['attach_type'] = 'Картинка'

            # Получаем файл
            pic_info = await dp.bot.get_file(msg.photo[-1].file_id)
            # Разделяем полученный файл на имя и расширение
            pic_name, pic_extension = os.path.splitext(pic_info.file_path)
            # Скачиваем файл
            download_pic = await dp.bot.download_file(pic_info.file_path)
            # Указываем путь и имя файла
            # Храним картинки с UID в имени, потому что он короче
            pic_src = 'photos/' + pic_info.file_unique_id + pic_extension
            
            # Сохраняем в базе
            await save_attach(data['ask_id'], pic_info.file_unique_id + pic_extension, 'Картинка', 'user', 'no')
            
            # Сохраняем в каталог
            with open(pic_src, 'wb') as new_pic:
                new_pic.write(download_pic.getvalue())

    # Если отправлено текстовое сообщение
    if msg.content_type == 'text' and len(msg.text) > 0:
        if data['attach_type'] is None:
            # Без вложений
            async with state.proxy() as data:
                data['msg'] = msg.text
                data['have_attach'] = 'нет'
        else:
            # С вложениями
            async with state.proxy() as data:
                data['msg'] = msg.text
                data['have_attach'] = 'да'

        # region завершаем заявку

        # Сообщение для пользователя
        await msg.answer(
            f'Заявка #{data["ask_id"]} успешно создана! Подробности:\n\n' +
            f'Имя пользователя: <b>{data["name"]}</b>\n' +
            f'Тема: <b>{data["theme"]}</b>\n' +
            f'Код ошибки: <b>{data["err_code"]}</b>\n' +
            f'Сообщение: \n\n{data["msg"]}\n\n' +
            f'После рассмотрения ты получишь уведомление :)',
            reply_markup=await upanel_kb() 
        )

        # Сообщение в саппорт-чат
        await dp.bot.send_message(
            SUPPORT_CHAT,
            f'Поступила заявка от @{msg.from_user.username}\n\n' +
            f'Номер заявки: <b>{data["ask_id"]}</b>\n' + 
            f'Имя пользователя: <b>{data["name"]}</b>\n' + 
            f'Тема: <b>{data["theme"]}</b>\n' +
            f'Код ошибки: <b>{data["err_code"]}</b>\n' + 
            f'Вложения: <b>{data["have_attach"]}</b>\n' +
            f'Тип вложений: <b>{data["attach_type"]}</b>\n' +
            f'Текст: \n\n<b>{data["msg"]}</b>\n\n' + 
            f'Чтобы посмотреть список открытых заявок <b>(ТГ)</b> - введите /asks или воспользуйтесь клавиатурой.'
        )

        await state.finish()

        # Сохраняем заявку в базе
        await request_reg('finish', data['ask_id'], msg.from_user.username, msg.from_user.id, data['name'], data['theme'], data['err_code'], data['msg'], data['have_attach'], data['attach_type'])
        # endregion
