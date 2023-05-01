import json
import string

from aiogram import types, Dispatcher


async def on_startup(_):
    print('Бот вышел в онлайн')


async def censor_messages(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(json.load(open('cenz.json'))):
        await message.reply('Маты запрещены!')
        await message.delete()


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(censor_messages)
