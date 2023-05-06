from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from pytube import YouTube
load_dotenv('.env')
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

buttons = [
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb.add(KeyboardButton("1"))

class VideoState(StatesGroup):
    download = State()


@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}!\nЯ Вам помогу скачать видео и аудио", reply_markup=keyboard_one)
executor.start_polling(dp, skip_updates=True)

@dp.message_handler(commands='video')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и я Вам его скачаю в mp4 формате")
    await VideoState.download.set()

@dp.message_handler(state=VideoState.download)
async def dowload_video(message:types.Message, state:FSMContext):
    await message.answer("Я Вас понял")
    await state.finish()

# https://youtu.be/lVilQl7Gv7o
# Машинное состояние


@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я Вас не понял")

executor.start_polling(dp, skip_updates=True)