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


async def on_startup(_):
    print('Бот вышел в онлайн')

'''**********************************CLIENT PART**********************************'''

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита!')
        await message.delete()
    except Exception:
        await message.reply('Общение с ботом через ЛС, напишите ему:'
                            '\n https://t.me/andrulik_pizzachef_bot')

@dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


@dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


'''**********************************ADMIN PART**********************************'''


'''**********************************GENERAL PART**********************************'''

@dp.message_handler()
async def echo(message: types.Message):
    # ждем пока в потоке не появится свободного места для выполнения данной команды
    await message.answer(message.text)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
