from aiogram_bot import dp, on_startup
from aiogram.utils import executor

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)