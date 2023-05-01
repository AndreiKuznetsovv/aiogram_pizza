from os import path, environ

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

# load environment for our app
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

# creation of memory storage for FSM
storage = MemoryStorage()

# creation of bot and dispatcher objects
bot = Bot(token=environ.get('TOKEN'))
dp = Dispatcher(bot, storage=storage)

from .handlers import client, admin, general

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
general.register_handlers_general(dp)

from .handlers.general import on_startup
