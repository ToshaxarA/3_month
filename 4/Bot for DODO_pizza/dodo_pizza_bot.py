from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os, sqlite3

load_dotenv('.env')
# Инициализация бота и хранилища состояний
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)


phone_button = [
    KeyboardButton('Отправить номер телефона', request_location=True)
]
phone = ReplyKeyboardMarkup(resize_keyboard=True).add(*phone_button)
# Определение функции для создания встроенной клавиатуры
def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Отправить номер", callback_data="send_phone_number"))
    keyboard.add(InlineKeyboardButton("Отправить локацию", callback_data="send_location"))
    keyboard.add(InlineKeyboardButton("Заказать еду", callback_data="order_food"))
    return keyboard





class OrderFoodState(StatesGroup):
    enter_title = State()
    enter_address = State()

# Создание подключения к базе данных
conn = sqlite3.connect('dodo_pizza.db')
cursor = conn.cursor()

# Создание таблиц в базе данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        id_user INTEGER,
        phone_number TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS address (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        address_longitude REAL,
        address_latitude REAL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        address_destination TEXT,
        date_time_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Проверка, существует ли пользователь в базе данных
    cursor.execute('SELECT * FROM users WHERE id_user=?', (message.from_user.id,))
    user = cursor.fetchone()

    if not user:
        # Если пользователь не существует, записываем его в базу данных
        cursor.execute('''
            INSERT INTO users (first_name, last_name, username, id_user)
            VALUES (?, ?, ?, ?)
        ''', (message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.id))
        conn.commit()

    # Отправка приветственного сообщения и inline-кнопок
    await message.reply(f"Здравствуйте, {message.from_user.full_name}!", reply_markup=get_inline_keyboard())
    await message.answer(f"Ниже кнопки, чтобы поделиться Вашим текущим местоположением и телефоном", reply_markup=phone)


@dp.message_handler(commands='send_phone_number')
async def send_phone_number(message:types.Message):
    # Обработка нажатия на кнопку "Послать телефонный номер"
    await message.answer("Взять Ваш номер?", reply_markup=phone)
    # await callback_query.message.answer("Введите название еды:")
    # await OrderFoodState.enter_title.set()

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    # Обработка нажатия на кнопку "Отправить номер"
    cursor.execute('UPDATE users SET phone_number=? WHERE id_user=?', (message.contact.phone_number, message.from_user.id))
    conn.commit()
    await message.reply("Спасибо! Ваш номер телефона сохранен.")


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message: types.Message):
    # Обработка нажатия на кнопку "Отправить локацию"
    cursor.execute('''
        INSERT INTO address (id_user, address_longitude, address_latitude)
        VALUES (?, ?, ?)
    ''', (message.from_user.id, message.location.longitude, message.location.latitude))
    conn.commit()
    await message.reply("Спасибо! Ваша локация сохранена.")

phone_button = [
    KeyboardButton('Отправить номер телефона', request_contact=True),
    KeyboardButton('Отправить своё местонахождение', request_location=True),
    ]
phone = ReplyKeyboardMarkup(resize_keyboard=True).add(*phone_button)



@dp.callback_query_handler(lambda query: query.data == 'send_phone_number')
async def send_phone_number(callback_query: types.CallbackQuery):

    # Обработка нажатия на кнопку "Заказать еду"
    await callback_query.message.answer("К сожалению эта кнопка в разработке, воспользуейтесь теми, что ниже для автоматического обмена информацией")
@dp.callback_query_handler(lambda query: query.data == 'send_location')
async def send_location(callback_query: types.CallbackQuery):

    # Обработка нажатия на кнопку "Заказать еду"
    await callback_query.message.answer("К сожалению эта кнопка в разработке, воспользуейтесь теми, что ниже для автоматического обмена информацией")

@dp.callback_query_handler(lambda query: query.data == 'order_food')
async def order_food(callback_query: types.CallbackQuery):

    # Обработка нажатия на кнопку "Заказать еду"
    await callback_query.message.answer("Введите название еды:")
    await OrderFoodState.enter_title.set()

@dp.message_handler(state=OrderFoodState.enter_title)
async def process_food_title(message: types.Message, state: FSMContext):
    # Обработка ввода названия еды
    async with state.proxy() as data:
        data['title'] = message.text

    await message.answer("Введите адрес доставки:")
    await OrderFoodState.next()


@dp.message_handler(state=OrderFoodState.enter_address)
async def process_food_address(message: types.Message, state: FSMContext):
    # Обработка ввода адреса доставки
    async with state.proxy() as data:
        data['address'] = message.text

    # Получение данных из контекста
    async with state.proxy() as data:
        title = data['title']
        address = data['address']

    # Запись данных в базу заказов
    cursor.execute('''
        INSERT INTO orders (title, address_destination)
        VALUES (?, ?)
    ''', (title, address))
    conn.commit()
    await message.answer("Ваш заказ принят!")
     

executor.start_polling(dp, skip_updates=True)

