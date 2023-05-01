from os import path, environ

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv


# load environment for our app
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

bot = Bot(token=environ.get('TOKEN'))
dp = Dispatcher(bot)

from .handlers.general import on_startup
