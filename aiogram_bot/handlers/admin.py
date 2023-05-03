from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram_bot import bot
from aiogram_bot.db_client.sqlite3_db import (
    db_add_command,
    db_delete_command,
    db_get_row_menu,
)
from aiogram_bot.keyboards import kb_admin
from aiogram_bot.states import FSMAdmin

# в моем случае 530176411
ID = None


# Получаем ID текущего модератора
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Чего надобно хозяин?', reply_markup=kb_admin)
    # await message.delete()


# Начало диалога загрузки нового пункта меню
async def command_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите фото')


async def command_cancel(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отмена произошла успешно')


# ловим первый ответ и пишем в словарь
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await FSMAdmin.next()
    await message.reply('Теперь введите название')


# Ловим второй ответ
async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FSMAdmin.next()
    await message.reply('ВВедите описание')


# Ловим третий ответ
async def load_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await FSMAdmin.next()
    await message.reply('Теперь укажи цену')


# Ловим последний ответ и используем полученные данные
async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)

    await db_add_command(state=state)
    await state.finish()


async def delete_callback(callback_query: types.CallbackQuery):
    await db_delete_command(callback_query.data.replace('del', ''))
    await callback_query.answer(text=f'Пицца {callback_query.data.replace("del ", "")} удалена.',
                                show_alert=True)
    p = 1


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        row_menu = await db_get_row_menu()
        for pizza in row_menu:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=pizza[0],
                                 caption=f'Название: {pizza[1]}\n'
                                         f'Описание: {pizza[2]}\n'
                                         f'Цена: {pizza[3]}$'
                                 )
            await bot.send_message(chat_id=message.from_user.id,
                                   text="^^^",
                                   reply_markup=types.InlineKeyboardMarkup().add(
                                       types.InlineKeyboardButton(
                                           f"Удалить пиццу {pizza[1]}",
                                           callback_data=f'del {pizza[1]}'
                                       )
                                   )
                                   )


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['Администратор'], is_chat_admin=True)
    dp.register_message_handler(command_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(command_cancel, commands=['Отмена'], state="*")
    dp.register_message_handler(command_cancel, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_callback_query_handler(delete_callback, lambda x: x.data and x.data.startswith('del'))
    dp.register_message_handler(delete_item, commands=['Удалить'])
