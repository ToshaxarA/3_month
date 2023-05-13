from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



from dotenv import load_dotenv
import os
# Инициализация бота и диспетчера
load_dotenv('.env')

bot = Bot(os.environ.get('token'))   # В файл .env нужно прописать "export token=..."
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
buttons = [
    KeyboardButton('/backend'), 
    KeyboardButton('/frontend'),
    KeyboardButton('/uxui'),
    KeyboardButton('/android'),
    KeyboardButton('/ios')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(*buttons)

class MailingState(StatesGroup):
    mail_text = State()

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.reply(f"Привет {message.from_user.full_name}! Я бот для IT курса, предназначен для предоставления информации о IT курсах.", reply_markup=keyboard_one)

@dp.message_handler(commands='frontend')
async def get_url_video(message:types.Message):
    await message.reply("Frontend — это внешняя часть сайта и клиентская часть приложения и т.д.\nСтоимость: 8000 сом в месяц\nОбучение: 4 месяца")

@dp.message_handler(commands='uxui')
async def get_url_video(message:types.Message):
    await message.reply('UX/UI — это разработка пользовательского интерфейса и опыта пользователя и т.д.\nСтоимость: 12000 сом в месяц\nОбучение: 6 месяцев')

@dp.message_handler(commands='android')
async def get_url_video(message:types.Message):
    await message.reply('Android — это разработка мобильных приложений под Android-устройства и т.д.\nСтоимость: 15000 сом в месяц\nОбучение: 7 месяцев')
    
@dp.message_handler(commands='ios')
async def get_url_video(message:types.Message):
    await message.reply('iOS — это разработка мобильных приложений под устройства Apple и т.д.\nСтоимость: 16000 сом в месяц\nОбучение: 8 месяцев')

@dp.message_handler(commands='backend')
async def get_url_video(message:types.Message):
    await message.reply('Backend — это внутренняя часть сайта и сервера и т.д.\nСтоимость: 10000 сом в месяц\nОбучение: 5 месяцев')
# # Обработчик команды "/start"
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     # Создаем клавиатуру с кнопками
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.row(
#         types.InlineKeyboardButton("Backend", callback_data='backend'),
#         types.InlineKeyboardButton("Frontend", callback_data='frontend')
#     )
#     keyboard.row(
#         types.InlineKeyboardButton("UX/UI", callback_data='uxui'),
#         types.InlineKeyboardButton("Android", callback_data='android')
#     )
#     keyboard.row(types.InlineKeyboardButton("iOS", callback_data='ios'))

#     # Отправляем приветственное сообщение с кнопками
#     await message.reply_text('Привет! Выбери одну из категорий:', reply_markup=keyboard)

# # Обработчик нажатия кнопок
# @dp.callback_query_handler(lambda callback_query: True)
# async def button(callback_query: types.CallbackQuery):
#     category = callback_query.data

#     if category == 'backend':
#         await message.answer('Backend — это внутренняя часть сайта и сервера и т.д.\nСтоимость: 10000 сом в месяц\nОбучение: 5 месяцев')
#     elif category == 'frontend':
#         message = 'Frontend — это внешняя часть сайта и клиентская часть приложения и т.д.\nСтоимость: 8000 сом в месяц\nОбучение: 4 месяца'
#     elif category == 'uxui':
#         message = 'UX/UI — это разработка пользовательского интерфейса и опыта пользователя и т.д.\nСтоимость: 12000 сом в месяц\nОбучение: 6 месяцев'
#     elif category == 'android':
#         message = 'Android — это разработка мобильных приложений под Android-устройства и т.д.\nСтоимость: 15000 сом в месяц\nОбучение: 7 месяцев'
#     elif category == 'ios':
#         message = 'iOS — это разработка мобильных приложений под устройства Apple и т.д.\nСтоимость: 16000 сом в месяц\nОбучение: 8 месяцев'
#     else:
#         message = 'Извините, произошла ошибка.'

    # Отправляем информацию о выбранной категории
    await bot.send_message(callback_query.from_user.id, text=message)

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял, попробуйте посмотреть команды с помощью /start")


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)