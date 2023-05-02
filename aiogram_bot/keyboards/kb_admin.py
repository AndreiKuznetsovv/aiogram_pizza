from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b_load = KeyboardButton('/Загрузить')
b_delete = KeyboardButton('/Удалить')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b_load).add(b_delete)