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



time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$')
# Создаем подключение к базе данных
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

# Создаем таблицу для списка дел, если она еще не существует

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER,
        user_id INTEGER,
        task TEXT,
        time TEXT
);
""")



conn.commit()
load_dotenv('.env')
# Инициализируем бота и диспетчера
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_keyboards1 = [
    InlineKeyboardButton('Добавить задание', callback_data='add_task'),
    InlineKeyboardButton('Удалить задание', callback_data='delete_task')
]

inline = InlineKeyboardMarkup().add(*inline_keyboards1)
inline2 = InlineKeyboardMarkup().add(*inline_keyboards1)


class Task_State(StatesGroup):
    task = State()
    time_task = State()
    delete_task = State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    image_url = 'https://quasa.io/storage/photos/%D0%A4%D0%BE%D1%82%D0%BE/00%20%D0%9F%D0%BB%D0%B0%D0%BD%207%20(1).png'

    # Загружаем изображение по URL
    response = requests.get(image_url)
    response.raise_for_status()
    # Создаем временный файл для сохранения изображения
    with open('temp_image.jpg', 'wb') as file:
        file.write(response.content)
    # Открываем временный файл с изображением
    with open('temp_image.jpg', 'rb') as photo:
        # Отправляем изображение пользователю
        await bot.send_photo(message.chat.id, photo)
    # Удаляем временный файл
    os.remove('temp_image.jpg')
    await message.answer(f"Привет {message.from_user.first_name}! Я бот планировщик твоих задач, умею записывать и удалять дела.", reply_markup=inline)

@dp.callback_query_handler(lambda query: query.data == 'add_task')
async def add_task(callback_query: types.CallbackQuery):

    # Обработка нажатия на кнопку "Добавить задание"
    await callback_query.message.answer("Введите описание дела:")
    await Task_State.task.set()

@dp.message_handler(state=Task_State.task)
async def process_task(message: types.Message, state: FSMContext):
    # Обработка ввода задачи
    async with state.proxy() as data:
        data['add_task'] = message.text
        

    await message.answer("Введите время для указанной задачи в формате часы:минуты:секунды, например 20:25:10:")
    await Task_State.time_task.set()


@dp.message_handler(state=Task_State.time_task)
async def process_time_choosing(message: types.Message, state: FSMContext):
    # Обработка ввода времени задачи
    
    async with state.proxy() as data:
        data['add_time'] = message.text.strip() 
            
                # Получение данных из контекста
    async with state.proxy() as data:
        time = data['add_time']
        task = data['add_task']
        
    # Запись данных в базу заказов
        cursor.execute('''
        INSERT INTO users (user_id, task, time)
        VALUES (?, ?, ?)
        ''', (message.from_user.id, task, time ))
        conn.commit()
        await message.answer("Ваша задача записана!", reply_markup=inline2)
        await state.finish()

@dp.callback_query_handler(lambda query: query.data == 'delete_task')
async def add_task(callback_query: types.CallbackQuery):

    # Обработка нажатия на кнопку "Удалить задание"
    await callback_query.message.answer("Введите id Вашего дела, которое хотите удалить:")
    await Task_State.delete_task.set()

@dp.message_handler(state=Task_State.delete_task)
async def delete_task(message: types.Message, state: FSMContext):
# Обработка ввода id задачи
    # del_data['add_del'] = message.text


    # Установка соединения с базой данных
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()

    # cursor.execute("SELECT COUNT(*) FROM users")
    # row_count = cursor.fetchone()[0]
    # print(row_count)

    # for i in range(row_count):
    #     show = "SELECT * FROM users WHERE id = ?"
    #     cursor.execute(show, (i))
    #     row1 = cursor.fetchone()
    #     await message.answer(f"{show}")

    # Запрос для удаления записи
    record_num = message.text  # Идентификатор записи, которую нужно удалить
    query = "DELETE FROM users WHERE id = ?"

    query_show = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query_show, (record_num,))
    row = cursor.fetchone()

    # Выполнение запроса с передачей параметров
    cursor.execute(query, (record_num,))
    conn.commit()
    
    # Закрытие соединения с базой данных
    conn.close()
    
    
    await message.answer(f"Указанная задача №'{row[0]}' удалена!")


#     async with state.proxy() as data:
#         data['add_time'] = message.text.strip()
    await state.finish()


# conn = sqlite3.connect('todo_list.db')
# cursor = conn.cursor()        
# cursor.execute("SELECT * FROM todo_list WHERE time = ?", (current_time,))
# task = cursor.fetchone()

executor.start_polling(dp, skip_updates=True)