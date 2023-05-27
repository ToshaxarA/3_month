import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule as schedule
from dotenv import load_dotenv
import sqlite3, os

# Создаем подключение к базе данных
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

# Создаем таблицу для списка дел, если она еще не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        time TEXT
    )
''')
conn.commit()
load_dotenv('.env')
# Инициализируем бота и диспетчера
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Обработчик команды /start
    Приветствует пользователя и предлагает помощь
    """
    await message.reply("Привет! Я ToDo List Bot. Чем я могу тебе помочь?\n"
                        "Чтобы добавить задание, отправь мне сообщение в формате: /add <title> <time>\n"
                        "Например: /add Помыть посуду 14:00\n"
                        "Чтобы удалить задание, отправь мне сообщение в формате: /remove <task_id>\n"
                        "Например: /remove 1")


@dp.message_handler(commands=['add'])
async def add_task(message: types.Message):
    """
    Обработчик команды /add
    Добавляет новое задание в список дел пользователя
    """
    try:
        command, title, time = message.text.split(maxsplit=2)
        user_id = message.from_user.id

        # Вставляем задание в базу данных
        cursor.execute('INSERT INTO tasks (user_id, title, time) VALUES (?, ?, ?)', (user_id, title, time))
        conn.commit()

        await message.reply(f"Задание '{title}' успешно добавлено на время {time}")
    except ValueError:
        await message.reply("Неправильный формат команды. Используй: /add <title> <time>")


@dp.message_handler(commands=['remove'])
async def remove_task(message: types.Message):
    """
    Обработчик команды /remove
    Удаляет задание из списка дел пользователя по его идентификатору
    """
    try:
        command, task_id = message.text.split(maxsplit=1)
        user_id = message.from_user.id

        # Удаляем задание из базы данных
        cursor.execute('DELETE FROM tasks WHERE id=? AND user_id=?', (task_id, user_id))
        conn.commit()

        await message.reply(f"Задание с идентификатором {task_id} успешно удалено")
    except ValueError:
        await message.reply("Неправильный формат команды. Используй: /remove <task_id>")

async def send_task_list(user_id: int):
    """
    Отправляет список дел пользователя по времени
    """
    # Получаем список дел пользователя из базы данных
    cursor.execute('SELECT * FROM tasks WHERE user_id=?', (user_id,))
    tasks = cursor.fetchall()

    if tasks:
        for task in tasks:
            task_id, _, title, time = task
            await bot.send_message(user_id, f"Задание #{task_id}: {title}")

    else:
        await bot.send_message(user_id, "У вас нет заданий в списке")


async def check_tasks():
    """
    Проверяет задания пользователя по времени и отправляет их список
    """
    cursor.execute('SELECT DISTINCT user_id FROM tasks')
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        user_id = user_id[0]
        cursor.execute('SELECT * FROM tasks WHERE user_id=?', (user_id,))
        tasks = cursor.fetchall()

        for task in tasks:
            _, _, _, time = task
            schedule.every().day.at(time).do(send_task_list, user_id)

    # Запускаем планировщик
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


# Запускаем бота
if __name__ == '__main__':
    asyncio.run(executor.start_polling(dp, skip_updates=True))