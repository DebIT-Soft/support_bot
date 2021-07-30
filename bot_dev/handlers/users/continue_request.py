from aiogram.types.callback_query import CallbackQuery
from keyboards.inline.support_inline import work_with_user_answer
import os

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import ContentType, Message
from data.config import SUPPORT_CHAT
from keyboards.default.upanel import *
from keyboards.inline.user_inline import *
from loader import dp
from states.all_states import Request, uAnswer
from utils.db_work.asks_tools.decline_request import decl_request
from utils.db_work.auth_tools.is_user_authorized import is_authorized
from utils.db_work.asks_tools.request_register import request_reg
from utils.db_work.asks_tools.saving_attachs import save_attach
from utils.db_work.asks_tools.processing_attachs import get_attachs, edit_attach_status
from aiogram.types.input_media import InputMediaDocument, InputMediaPhoto
import re
from utils.db_work.asks_tools.saving_answer import save_answer

""" Взаимодействие с ответом на заявку """
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('cont_ask'))
async def user_continue(callback_query: CallbackQuery, state: FSMContext):
    # Выгружаем полученные callback_data в список
    cb_data = []
    for item in callback_query.data.split(":"):
        if not item.strip():
            continue
        cb_data.append(item.strip())
    
    # Убираем кнопки
    await dp.bot.edit_message_reply_markup(
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=None
        )

    # Проверяем, не истек ли срок ответа
    time_info = []
    time_exp = []
    for item in cb_data[4].split(" "):
        if not item.strip():
            continue
        time_info.append(item.strip())
    
    if len(time_info) > 1:
        time_info.pop(0)
    
    for item in str(time_info).split(":"):
        if not item.strip():
            continue
        time_exp.append(item.strip())
    
    if int(str(time_exp[0]).replace("[\'", '').replace("\']", '')) < 1:
        await dp.bot.send_message(callback_query.from_user.id, 'Упс... Прошел час, заявка уже закрыта.')
    else:
        # Нажата кнопка ответить
        if cb_data[1] == 'answer':
            await dp.bot.send_message(
                cb_data[3],
                f'Ожидаю ответ на заявку #{cb_data[2]}...\n\n' +
                f'Если к ответу будут прикреплены картинки или документы, то сначала отправь мне их, а после - ' +
                f'само сообщение.\nЕсли же к сообщению ничего прикрепляться не будет, то просто отправь текст ответа 🙂\n\n' +
                f'<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>'
            )

            await uAnswer.attach_type.set()
            async with state.proxy() as data:
                data['attach_type'] = None
                data['ask_id'] = cb_data[2]

            await uAnswer.msg.set()

        # Нажата кнопка завершить
        if cb_data[1] == 'close':
            await dp.bot.send_message(
                cb_data[3],
                f'Заявка #{cb_data[2]} успешно завершена :)',
                reply_markup=await upanel_kb()
            )

            await dp.bot.send_message(
                SUPPORT_CHAT,
                f'@{callback_query.from_user.username} закрыл заявку.'
            )

""" Получаем ответ от пользователя """
@dp.message_handler(state=uAnswer.msg, content_types=ContentType.PHOTO)
@dp.message_handler(state=uAnswer.msg, content_types=ContentType.TEXT)
@dp.message_handler(state=uAnswer.msg, content_types=ContentType.DOCUMENT)
async def get_user_answer(msg: Message, state: FSMContext):
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
        await msg.answer('Ответ отправлен.')
        if data['attach_type'] is None:
            # Без вложений
            async with state.proxy() as data:
                data['msg'] = msg.text
                data['have_attach'] = 'нет'

            await dp.bot.send_message(
                SUPPORT_CHAT,
                f'@{msg.from_user.username} продолжает общение по заявке #{data["ask_id"]}.\n\n{data["msg"]}',
                reply_markup=await work_with_user_answer(data['ask_id'], msg.from_user.id)
            )
        else:
            # С вложениями
            async with state.proxy() as data:
                data['msg'] = msg.text
                data['have_attach'] = 'да'

            await dp.bot.send_message(
                SUPPORT_CHAT,
                f'@{msg.from_user.username} продолжает общение по заявке #{data["ask_id"]}.\n\n{data["msg"]}',
                reply_markup=await work_with_user_answer(data['ask_id'], msg.from_user.id)
            )

            # Получаем вложения
            files = await get_attachs(data['ask_id'], 'user', 'no')
            attach = ''
            # Проверяем их по типу
            if re.search('Документ', str(files)):
                # Прикрепляем первый с подписью
                attach = [InputMediaDocument(open(f'documents/{files[0]["name"]}', 'rb'), caption=f"Вложения к заявке #{data['ask_id']}")]
                    
                # Прикрепляем остальные
                for item in range(1, len(files)):
                    attach.insert(0, InputMediaDocument(open(f'documents/{files[item]["name"]}', 'rb')))
            if re.search('Картинка', str(files)):
                # Прикрепляем первую с подписью
                attach = [InputMediaPhoto(open(f'photos/{files[0]["name"]}', 'rb'), caption=f"Вложения к заявке #{data['ask_id']}")]
                
                # Прикрепляем остальные
                for item in range(1, len(files)):
                    attach.append(InputMediaPhoto(open(f'photos/{files[item]["name"]}', 'rb')))
            try:
                await dp.bot.send_media_group(SUPPORT_CHAT, attach)
            except Exception as e:
                await dp.bot.send_message(SUPPORT_CHAT, f'Ошибка при отправке альбома.\nФайл: handlers/users/continue_request.py\nМетод: get_user_answer\n\nНеобходимо проверить базу.\nПодробности:\n\n{str(e)}')
            await edit_attach_status(data["ask_id"], 'user')
        
        # Записываем ответ юзера
        await save_answer(data['ask_id'], data['have_attach'], msg.from_user.username, None, data['msg'], None)
        
        await state.finish()
