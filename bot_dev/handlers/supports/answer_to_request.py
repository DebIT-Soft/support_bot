from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMediaDocument, InputMediaPhoto
from keyboards.inline.user_inline import continue_request_kb
from aiogram.types.message import ContentType, Message
import os
from utils.db_work.asks_tools.pin_ask_to_supp import pin_ask
from utils.db_work.asks_tools.processing_attachs import get_attachs, edit_attach_status
from utils.db_work.asks_tools.resetting_request import ask_reset
from utils.db_work.asks_tools.saving_attachs import save_attach
from utils.db_work.asks_tools.closing_request import close_request
import re
from states.all_states import supportKB

from aiogram.dispatcher.storage import FSMContext
from utils.db_work.asks_tools.getting_ask_info import get_ask_info
from data.config import ADMINS, SUPPORTS, SUPPORT_CHAT
from aiogram.dispatcher.filters import Text
from aiogram import types
from keyboards.inline.support_inline import *
from loader import dp

""" Выбор заявки """
@dp.message_handler(state=supportKB.ask)
async def process_req(msg: Message, state: FSMContext):
    if msg.from_user.id in SUPPORTS or msg.from_user.id in ADMINS:
        ask_id = msg.text.replace('✉️ Заявка #', '')

        await msg.answer(f'Загружаю информацию по заявке #{ask_id}...')

        ask_info, user_id = await get_ask_info(ask_id)

        await msg.answer(f'{ask_info}', reply_markup=await work_with_request(ask_id, user_id))

        # Если у заявки есть вложения, то получаем их
        if re.search('Вложения: <b>да</b>', ask_info):
            attach = None
            # Список вложений
            files = await get_attachs(ask_id, 'user', 'no')
            # Если вложение - картинка
            if re.search('Картинка', ask_info):
                # Прикрепляем первую с подписью
                attach = [InputMediaPhoto(open(f'photos/{files[0]["name"]}', 'rb'), caption=f'Вложения к заявке #{ask_id}')]

                # Прикрепляем остальные
                for item in range(1, len(files)):
                    attach.append(InputMediaPhoto(open(f'photos/{files[item]["name"]}', 'rb')))

            # Если вложение - документ
            if re.search('Документ', ask_info):
                # Прикрепляем первый с подписью
                attach = [InputMediaDocument(open(f'documents/{files[0]["name"]}', 'rb'), caption=f'Вложения к заявке #{ask_id}')]
                
                # Прикрепляем остальные
                for item in range(1, len(files)):
                    attach.insert(0, InputMediaDocument(open(f'documents/{files[item]["name"]}', 'rb')))
            
            try:
                await dp.bot.send_media_group(SUPPORT_CHAT, attach)
            except Exception as e:
                await dp.bot.send_message(SUPPORT_CHAT, f'Ошибка при отправке альбома.\nФайл: handlers/supports/answer_to_request.py\nМетод: process_req\n\nНеобходимо проверить базу.\nПодробности:\n\n{str(e)}')
            

        # Привязываем заявку к оператору
        await pin_ask(msg.from_user.username, ask_id)
        
        await supportKB.curr_support.set()
        async with state.proxy() as data:
            data['curr_support'] = msg.from_user.username

        await supportKB.get_ans.set()

""" Работа с заявкой """
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('req_proc'), state=supportKB.get_ans)
async def cb_work_with_req(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in SUPPORTS or callback_query.from_user.id in ADMINS:

        # Выгружаем полученные callback_data в список
        cb_data = []
        for item in callback_query.data.split(":"):
            if not item.strip():
                continue
            cb_data.append(item.strip())

        # Нажата кнопка закрыть
        if cb_data[1] == 'close':
            await state.finish()

            for msg_id in range(0, int(cb_data[4]) + 1):
                await dp.bot.delete_message(
                    SUPPORT_CHAT, callback_query.message.message_id + msg_id
                )

            await ask_reset(cb_data[2])
        else:
            curr_support = ''
            async with state.proxy() as data:
                curr_support = data['curr_support']
                data['ask_id'] = cb_data[2]
                data['attach_type'] = None
                data['user_id'] = cb_data[3]

            # Проверка, тот ли оператор хочет ответить или отклонить заявку
            if callback_query.from_user.username == curr_support:

                # Нажата кнопка ответить
                if cb_data[1] == 'answer':
                    
                    await dp.bot.send_message(
                        SUPPORT_CHAT,
                        f"@{callback_query.from_user.username}, ожидаю ответ на заявку #{cb_data[2]}...\n\n" +
                        f"Если к ответу будут прикреплены картинки или документы, то сначала отправь мне их, а после - " +
                        f"само сообщение.\nЕсли же к сообщению ничего прикрепляться не будет, то просто отправь текст ответа 🙂\n\n" +
                        f"<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>"
                    )

                    await dp.bot.edit_message_text(
                        f'{callback_query.message.text}\n\nНа заявку ответил(-а) @{callback_query.from_user.username}',
                        SUPPORT_CHAT, callback_query.message.message_id
                    )

                    await edit_attach_status(data["ask_id"], 'user')


                    async with state.proxy() as data:
                        data['action'] = 'answer'

                # Нажата кнопка отклонить
                if cb_data[1] == 'cancel':
                    await dp.bot.send_message(
                        SUPPORT_CHAT,
                        f"@{callback_query.from_user.username}, ожидаю причину, по которой отклонена заявка #{cb_data[2]}...\n\n" +
                        f"Если к ответу будут прикреплены картинки или документы, то сначала отправь мне их, а после - " +
                        f"само сообщение.\nЕсли же к сообщению ничего прикрепляться не будет, то просто отправь текст ответа 🙂\n\n" +
                        f"<i>P.S.: К заявке можно прикрепить вложения только 1 типа - картинки или документы.</i>"
                    )

                    await dp.bot.edit_message_text(
                        f'{callback_query.message.text}\n\nЗаявку отклонил(-а) @{callback_query.from_user.username}',
                        SUPPORT_CHAT, callback_query.message.message_id
                    )

                    async with state.proxy() as data:
                        data['action'] = 'decline'

                
                await supportKB.msg.set()

""" Ответ на заявку/причина отказа """
@dp.message_handler(state=supportKB.msg, content_types=ContentType.PHOTO)
@dp.message_handler(state=supportKB.msg, content_types=ContentType.TEXT)
@dp.message_handler(state=supportKB.msg, content_types=ContentType.DOCUMENT)
async def get_request_answer(msg: Message, state: FSMContext):
    if msg.from_user.id in SUPPORTS or msg.from_user.id in ADMINS:
        curr_support = ''
        async with state.proxy() as data:
            curr_support = data['curr_support']

        if msg.from_user.username == curr_support:
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
                await msg.answer(f'Ответ на заявку #{data["ask_id"]} отправлен пользователю.')
                
                if data['attach_type'] is None:
                    # Без вложений
                    async with state.proxy() as data:
                        data['msg'] = msg.text
                        data['have_attach'] = 'нет'

                    if data['action'] == 'decline':
                        await dp.bot.send_message(
                            data['user_id'],
                            f'Заявка #{data["ask_id"]} была отклонена. Причина:\n\n{data["msg"]}'
                        )
                    else:
                        await dp.bot.send_message(
                            data['user_id'],
                            f'Заявка #{data["ask_id"]} была рассмотрена. Ответ:\n\n{data["msg"]}\n\n<i>Если вопрос не был решен - нажми на кнопку \"Ответить\".\n' +
                            f'Если же вопрос был решен, то нажми кнопку \"Завершить\" :).\nP.S.: Заявка будет автоматически закрыта через час.</i>',
                            reply_markup=await continue_request_kb(data['ask_id'], data['user_id'])
                        )
                    await state.finish()
                else:
                    # С вложениями
                    async with state.proxy() as data:
                        data['msg'] = msg.text
                        data['have_attach'] = 'да'

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
                        
                    if data['action'] == 'decline':
                        await dp.bot.send_message(
                            data['user_id'],
                            f'Заявка #{data["ask_id"]} была отклонена. Причина:\n\n{data["msg"]}'
                        )

                        # Закрываем заявку
                        await close_request(data['ask_id'], 'отклонен')
                    else:
                        await dp.bot.send_message(
                            data['user_id'],
                            f'Заявка #{data["ask_id"]} была рассмотрена. Ответ:\n\n{data["msg"]}\n\n<i>Если вопрос не был решен - нажми на кнопку \"Ответить\".\n' +
                            f'Если же вопрос был решен, то нажми кнопку \"Завершить\" :).\nP.S.: Заявка будет автоматически закрыта через час.</i>',
                            reply_markup=await continue_request_kb(data['ask_id'], data['user_id'])
                        )

                        # Закрываем заявку
                        await close_request(data['ask_id'], 'закрыт')
                        

                    user_id = data['user_id']
                    ask_id = data['ask_id']

                    await state.finish()

                    # Отправляем вложения
                    try:
                        await dp.bot.send_media_group(user_id, attach)
                    except Exception as e:
                        await dp.bot.send_message(SUPPORT_CHAT, f'Ошибка при отправке альбома.\nФайл: handlers/supports/answer_to_request.py\nМетод: get_request_answer\n\nНеобходимо проверить базу.\nПодробности:\n\n{str(e)}')
            
                    # Изменяем статус отправки вложений
                    await edit_attach_status(ask_id, 'support')

