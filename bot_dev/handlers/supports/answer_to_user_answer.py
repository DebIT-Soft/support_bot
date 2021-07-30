from aiogram.types.callback_query import CallbackQuery
from keyboards.inline.support_inline import work_with_user_answer
import os

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import ContentType, Message
from data.config import ADMINS, SUPPORTS, SUPPORT_CHAT
from keyboards.default.upanel import *
from keyboards.inline.user_inline import *
from loader import dp
from states.all_states import AnswerToAnswer, Request, uAnswer
from utils.db_work.asks_tools.decline_request import decl_request
from utils.db_work.auth_tools.is_user_authorized import is_authorized
from utils.db_work.asks_tools.request_register import request_reg
from utils.db_work.asks_tools.saving_attachs import save_attach
from utils.db_work.asks_tools.processing_attachs import get_attachs, edit_attach_status
from aiogram.types.input_media import InputMediaDocument, InputMediaPhoto
import re
from utils.db_work.asks_tools.saving_answer import save_answer

""" Взаимодействие с ответом на ответ :) """
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('scont_ask'))
async def answer_to_user(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in SUPPORTS or callback_query.from_user.id in ADMINS:
        # Выгружаем полученные callback_data в список
        cb_data = []
        for item in callback_query.data.split(":"):
            if not item.strip():
                continue
            cb_data.append(item.strip())
        
        # Убираем кнопки
        await dp.bot.edit_message_reply_markup(
                SUPPORT_CHAT,
                callback_query.message.message_id,
                reply_markup=None
            )
        
        # Нажата кнопка ответить
        if cb_data[1] == 'answer':
            await dp.bot.send_message(
                SUPPORT_CHAT,
                f'Ожидаю ответ на заявку #{cb_data[2]}...\n\n' +
                f'Если к ответу будут прикреплены картинки или документы, то сначала отправь мне их, а после - ' +
                f'само сообщение.\nЕсли же к сообщению ничего прикрепляться не будет, то просто отправь текст ответа 🙂\n\n' +
                f'<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>'
            )

            await AnswerToAnswer.curr_support.set()
            async with state.proxy() as data:
                data['attach_type'] = None
                data['ask_id'] = cb_data[2]
                data['curr_support'] = callback_query.from_user.username
                data['user_id'] = cb_data[3]

            await AnswerToAnswer.msg.set()

        # Нажата кнопка завершить
        if cb_data[1] == 'close':
            await dp.bot.send_message(
                SUPPORT_CHAT,
                f'Заявка #{cb_data[2]} закрыта.'
            )

            await dp.bot.send_message(
                cb_data[3],
                f'Оператор закрыл заявку #{cb_data[2]}.'
            )

""" Получаем ответ от оператора """
@dp.message_handler(state=AnswerToAnswer.msg, content_types=ContentType.PHOTO)
@dp.message_handler(state=AnswerToAnswer.msg, content_types=ContentType.TEXT)
@dp.message_handler(state=AnswerToAnswer.msg, content_types=ContentType.DOCUMENT)
async def get_answer_to_answer(msg: Message, state: FSMContext):
    if msg.from_user.id in SUPPORTS or msg.from_user.id in ADMINS:
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
                await save_attach(data['ask_id'], doc_info.file_unique_id + doc_extension, 'Документ', 'support', 'no')
                
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
                await save_attach(data['ask_id'], pic_info.file_unique_id + pic_extension, 'Картинка', 'support', 'no')
                
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
                    data['user_id'],
                    f'Поступил ответ на заявку #{data["ask_id"]}:\n\n{data["msg"]}',
                    reply_markup=await continue_request_kb(data['ask_id'], data['user_id'])
                )
            else:
                # С вложениями
                async with state.proxy() as data:
                    data['msg'] = msg.text
                    data['have_attach'] = 'да'

                await dp.bot.send_message(
                    data['user_id'],
                    f'Поступил ответ на заявку #{data["ask_id"]}:\n\n{data["msg"]}',
                    reply_markup=await continue_request_kb(data['ask_id'], data['user_id'])
                )

                # Получаем вложения
                files = await get_attachs(data['ask_id'], 'support', 'no')
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
                print(attach)
                print(files)
                try:
                    await dp.bot.send_media_group(data['user_id'], attach)
                except Exception as e:
                    await dp.bot.send_message(SUPPORT_CHAT, f'Ошибка при отправке альбома.\nФайл: handlers/supports/answer_to_answer.py\nМетод: get_answer_to_answer\n\nНеобходимо проверить базу.\nПодробности:\n\n{str(e)}')
                
                # await edit_attach_status(data["ask_id"], 'support')

            # Записываем ответ оператора
            await save_answer(data['ask_id'], data['have_attach'], None, msg.from_user.username, None, data['msg'])

            await state.finish()