import sqlite3

from aiogram import Bot
from aiogram import types


def start_db():
    global conn, cur
    conn = sqlite3.connect('./pizza.db')
    cur = conn.cursor()
    if conn:
        print('Data base connected OK!')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT);'
    )
    conn.commit()


async def db_add_command(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO menu VALUES (?, ?, ?, ?);',
            tuple(data.values())
        )
        conn.commit()


async def db_get_menu(message: types.Message, bot: Bot):
    for pizza in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=pizza[0],
                             caption=f'Название: {pizza[1]}\n'
                                     f'Описание: {pizza[2]}\n'
                                     f'Цена: {pizza[3]}$'
                             )


async def db_get_row_menu():
    return cur.execute('SELECT * FROM menu').fetchall()


async def db_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data.strip(),))
    conn.commit()