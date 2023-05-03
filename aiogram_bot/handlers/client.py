from aiogram import types, Dispatcher

from aiogram_bot import bot
from aiogram_bot.db_client.sqlite3_db import db_get_menu
from aiogram_bot.keyboards import kb_client


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита!', reply_markup=kb_client)
        await message.delete()
    except Exception:
        await message.reply('Общение с ботом через ЛС, напишите ему:'
                            '\n https://t.me/andrulik_pizzachef_bot')


async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


async def pizza_menu_command(message: types.Message):
    await db_get_menu(message=message, bot=bot)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
