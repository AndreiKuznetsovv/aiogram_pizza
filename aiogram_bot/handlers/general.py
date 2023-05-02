import json
import string

from aiogram import types, Dispatcher
from aiogram_bot.db_client import sqlite3_db

async def on_startup(_):
    sqlite3_db.start_db()
    print('Бот вышел в онлайн')


async def censor_messages(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(json.load(open('cenz.json'))):
        await message.reply('Маты запрещены!')
        await message.delete()


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(censor_messages)
