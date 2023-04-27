from os import path, environ

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

# load environment for our app
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

bot = Bot(token=environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    # ждем пока в потоке не появится свободного места для выполнения данной команды
    await message.answer(message.text)




executor.start_polling(dp, skip_updates=True)
