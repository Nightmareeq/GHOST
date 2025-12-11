import sqlite3
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.filters import Command

API_TOKEN = "8454172718:AAG7h65NsoWUi8nOTo_DLHYE_nIr31te84w"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT
            )
        ''')
    conn.commit()

def add_user(user_id: int, username: str):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        if not exists:
            try:
                cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
                conn.commit()
                print(f"✅ Добавлен новый пользователь: {username} ({user_id})")
            except sqlite3.IntegrityError:
                pass
        else:
            print(f"⚠ Пользователь уже существует: {username} ({user_id})")

def get_user_count():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
    return count

@dp.message(Command('start'))
async def starting_bot(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Без username"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть игру", web_app=WebAppInfo(url="https://tapquest-1.preview.emergentagent.com/"))]
    ])
    add_user(user_id, username)
    await message.answer("🎁ПРИСОЕДИНЯЙСЯ К ПРОЕКТУ И ПОЛУЧАЙ ПРИЗ В КОНЦЕ СЕЗОНА 👇", reply_markup=keyboard)

@dp.message(Command('users'))
async def show_user_count(message: Message):
    if message.chat.id == 640412206:
        count = get_user_count()
        await message.answer(f"👥 Количество пользователей: {count}")
    else:
        return

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())