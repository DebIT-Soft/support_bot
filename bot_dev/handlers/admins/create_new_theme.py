from utils.other.serialize_theme import serialize_theme
from aiogram.types.callback_query import CallbackQuery
from keyboards.inline.admin_inline import confirm_theme, edit_theme
from aiogram.dispatcher.storage import FSMContext
from states.all_states import newTheme
from data.config import THEMES
from aiogram.types.message import Message
from loader import dp


@dp.message_handler(commands='theme_add')
async def create_theme(msg: Message, state: FSMContext):
    await msg.answer('Отправь мне имя темы...')

    await newTheme.emoji_old.set()
    async with state.proxy() as data:
        data['emoji_old'] = 'NaN'
    
    await newTheme.theme.set()

@dp.message_handler(state=newTheme.theme)
async def get_theme_name(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['theme'] = msg.text
    
    if data['emoji_old'] == 'NaN':
        await msg.answer(
            'А теперь отправь мне смайлик, который будет отображаться слева. Или отправь 0, чтобы оставить тему без смайлика.'
            )        
    else:
        await msg.answer(
                    f'Новая тема обращения:\n{data["emoji_old"]} {data["theme"]} | {data["theme"]}',
                    reply_markup = await confirm_theme()
                )

    await newTheme.emoji.set()
    

@dp.message_handler(state=newTheme.emoji)
async def get_theme_emoji(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['emoji'] = msg.text
    
    await msg.answer(
        f'Новая тема обращения:\n{data["emoji"]} {data["theme"]} | {data["theme"]}',
        reply_markup = await confirm_theme()
        )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('theme'), state=newTheme.emoji)
async def processing_new_theme(callback_query: CallbackQuery, state: FSMContext):   
    if callback_query.data == 'theme:confirm':
        await callback_query.message.edit_text(
            'Сохраняю новую тему... :)'
        )

        async with state.proxy() as data:
            await serialize_theme(data['theme'], data['emoji'])

        await dp.bot.send_message(
            callback_query.message.chat.id,
            'Тема успешно сохранена :)'
        )
        await state.finish()
    
    elif callback_query.data == 'theme:edit':
        await callback_query.message.edit_text(
            'Что будем изменять?',
            reply_markup = await edit_theme()
            )

    elif callback_query.data == 'theme:emoji':
        await callback_query.message.edit_text(
            'Отправь мне новый смайлик :)'
            )

    elif callback_query.data == 'theme:name':
        await callback_query.message.edit_text(
            'Отправь мне новое имя темы :)'
        )

        await newTheme.emoji_old.set()
        async with state.proxy() as data:
            data['emoji_old'] = data['emoji']

        await newTheme.theme.set()

    elif callback_query.data == 'theme:back':
        async with state.proxy() as data:
            have_emoji = data['emoji_old']
        
        if have_emoji == 'NaN':
            await callback_query.message.edit_text(
                f'Новая тема обращения:\n{data["emoji"]} {data["theme"]} | {data["theme"]}',
                reply_markup = await confirm_theme()
            )
        else:
            await callback_query.message.edit_text(
                f'Новая тема обращения:\n{data["emoji_old"]} {data["theme"]} | {data["theme"]}',
                reply_markup = await confirm_theme()
            )

    elif callback_query.data == 'theme:decline':
        await callback_query.message.delete()
        await state.finish()