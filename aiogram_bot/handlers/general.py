import json
import string

from aiogram import types

from aiogram_bot import dp

async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler()
async def echo(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(json.load(open('cenz.json'))):
        await message.reply('Маты запрещены!')
        await message.delete()
