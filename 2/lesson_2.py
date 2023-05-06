import random
from aiogram import Bot, Dispatcher, types, executor
# from config import TOKEN_API
from dotenv import load_dotenv
import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
load_dotenv('.env')


bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb.add(KeyboardButton("1"))
kb.insert(KeyboardButton("2"))
kb.insert(KeyboardButton("3"))

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer("Привет! Я бот, который загадывает случайное число с помощью \
библиотеки random и вы должны угадать его.\n Давай начнём! /play - запустить игру")
    await message.delete()
    
@dp.message_handler(commands='help')
async def start(message:types.Message):
    await message.reply("Вот мои команды:\n/start - запустить бота\n /play - запустить игру")

@dp.message_handler(commands='play')
async def play(message:types.Message):

    await bot.send_message(chat_id=message.from_user.id,text="Я загадал число от 1 до 3 угадайте, какое?",
                            parse_mode="HTML", reply_markup=kb)
@dp.message_handler(content_types = 'text')
async def comp(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id,text="Я загадал:")
    x = random.randint(1,3)
    await bot.send_message(chat_id=message.from_user.id,text= x)
    if int(message.text) == x:
        await bot.send_message(chat_id=message.from_user.id,text="You WIN!")
    else:
        await bot.send_message(chat_id=message.from_user.id,text= "Try more")
    
@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял введите /help")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)