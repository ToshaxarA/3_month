# Телеграмм боты, парсинг данных, работа с базами данных
from aiogram import Bot, Dispatcher, types, executor

bot = Bot("6033434332:AAHWDc-SUkapRzzAiSGI-o8OM5dOt5O5bSU")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer("Привет! Вот мои команды:\n/start - запустить бота")
@dp.message_handler(commands='help')
async def start(message:types.Message):
    await message.reply("Вот мои команды:\n/start - запустить бота")

@dp.message_handler(text = ['Привет!'])
async def hello(message:types.Message):
    await message.reply(f"Привет {message.from_user.full_name}!")

@dp.message_handler(commands='test')
async def test(message:types.Message):
    await message.reply('Тест')
    await message.answer('Тест')
    await message.answer_location(40.51931947246192, 72.80297644427407)
    await message.answer_photo("https://coppellstudentmedia.com/wp-content/uploads/2016/03/nerdvgeek.jpg")
    with open('photo.png', 'rb') as photo:
        await message.answer_photo(photo)
    with open('lesson_.pdf', 'rb') as pdf:
        await message.answer_document(pdf)
    


@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял введите /help")

executor.start_polling(dp)

