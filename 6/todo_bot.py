import asyncio
import aioschedule as schedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import executor
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aioschedule as schedule
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import sqlite3, os, asyncio, requests, re, logging, requests, time

# Замените YOUR_TOKEN на ваш токен бота
load_dotenv('.env')
# Инициализируем бота и диспетчера
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


# Определяем состояния FSM
class AddTask(StatesGroup):
    title = State()
    time = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот для управления делами. Чтобы добавить дело, используй команду /addtask.")


# Обработчик команды /addtask
@dp.message_handler(commands=['addtask'])
async def cmd_addtask(message: types.Message):
    await AddTask.title.set()
    await message.reply("Введите название дела:")


# Обработчик сообщения с названием дела
@dp.message_handler(state=AddTask.title)
async def process_task_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await AddTask.next()
    await message.reply("Введите время выполнения дела (в формате ЧЧ:ММ):")


# Обработчик сообщения с временем выполнения дела
@dp.message_handler(state=AddTask.time)
async def process_task_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    # Сохраняем дело в базу данных
    save_task(data['title'], data['time'])

    await state.finish()
    await message.reply("Дело успешно добавлено!")


# Обработчик команды /list
@dp.message_handler(commands=['list'])
async def cmd_list(message: types.Message):
    tasks = get_tasks()
    if tasks:
        tasks_text = '\n'.join(tasks)
        await message.reply(f"Список дел:\n{tasks_text}")
    else:
        await message.reply("Список дел пуст.")


# Обработчик команды /delete
@dp.message_handler(commands=['delete'])
async def cmd_delete(message: types.Message):
    tasks = get_tasks()
    if tasks:
        keyboard_markup = InlineKeyboardMarkup()
        for task in tasks:
            button = InlineKeyboardButton(task, callback_data=task)
            keyboard_markup.add(button)

        await message.reply("Выберите дело для удаления:", reply_markup=keyboard_markup)
    else:
        await message.reply("Список дел пуст.")


# Обработчик нажатия на кнопку удаления дела
@dp.callback_query_handler(lambda callback_query: True)
async def process_delete_task(callback_query: types.CallbackQuery):
    task = callback_query.data
    delete_task(task)
    await bot.send_message(callback_query.from_user.id, f"Дело '{task}' удалено.")

import sqlite3

# Функция создания таблицы дел
def create_table():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция сохранения дела в базу данных
def save_task(title, time):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, time) VALUES (?, ?)', (title, time))
    conn.commit()
    conn.close()

# Функция получения списка дел из базы данных
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]

# Функция удаления дела из базы данных
def delete_task(task):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE title=?', (task,))
    conn.commit()
    conn.close()

# Создание таблицы при запуске программы
create_table()


@dp.callback_query_handler(lambda callback_query: True)
async def process_delete_task(callback_query: types.CallbackQuery):
    task = callback_query.data
    delete_task(task)
    await bot.send_message(callback_query.from_user.id, f"Дело '{task}' удалено.")


# Обработчик команды /delete
@dp.message_handler(commands=['delete'])
async def cmd_delete(message: types.Message):
    tasks = get_tasks()
    if tasks:
        keyboard_markup = InlineKeyboardMarkup()
        for task in tasks:
            button = InlineKeyboardButton(task, callback_data=task)
            keyboard_markup.add(button)

        await message.reply("Выберите дело для удаления:", reply_markup=keyboard_markup)
    else:
        await message.reply("Список дел пуст.")

# Функция отправки напоминания о делах
async def send_reminder(task):
    tasks = get_tasks()
    if task in tasks:
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=f"Напоминание: У вас запланировано дело '{task}'!")

# Функция для запуска планировщика напоминаний
async def start_reminder_scheduler():
    tasks = get_tasks()
    for task in tasks:
        task_time = get_task_time(task)
    if task_time:
        schedule.every().day.at(task_time).do(send_reminder, task=task)
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)
# Запускаем планировщик напоминаний
async def on_startup(dp):
    asyncio.create_task(start_reminder_scheduler())

executor.start_polling(dp, on_startup=on_startup)
