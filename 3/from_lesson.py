from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from dotenv import load_dotenv
import os, logging
import sqlite3
import time

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created VARCHAR(200)
);
""")
cursor.connection.commit()


buttons = [
    KeyboardButton('/video'),
    KeyboardButton('/audio')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

class MailingState(StatesGroup):
    mail_text = State()

@dp.message_handler(commands=['start'])
async def start(message:types.Message):
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.username}',
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{time.ctime()}'
        )""")
        cursor.connection.commit()  #Для сохранения в базе данных
    await message.answer(f"Привет {message.from_user.full_name}!\nЯ вам помогу скачать видео и аудио", reply_markup=keyboard_one)

class VideoState(StatesGroup):
    download = State()

# @dp.message_handler(commands='mail')
# async def get_mail_text

@dp.message_handler(commands='video')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на видео и я вам его скачаю в mp4 формате")
    await VideoState.download.set()
@dp.message_handler(commands='audio')
async def get_url_video(message:types.Message):
    await message.reply("Отправьте ссылку на аудио на Youtube и я вам его скачаю в mp3 формате")
    await VideoState.download.set()
    

@dp.message_handler(state=VideoState.download)
async def download_video(message: types.Message, state: FSMContext):
    url = message.text
    yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    yt.streams.filter(progressive=True, file_extension="mp4").first().download("video", f"{yt.title}.mp4")
    yt.streams.filter(only_audio=True).first().download("audio", f"{yt.title}.mp3")
    title = yt.title
    video = open(f"video/{title}.mp4", "rb")
    audio = open(f"audio/{title}.mp3", "rb")
    await message.reply("Видео и аудио загружаются")
    await bot.send_video(message.chat.id, video)
    await bot.send_audio(message.chat.id, audio)
    
    
    os.remove(f"video/{title}.mp4")
    os.remove(f"audio/{title}.mp3")
    await message.reply("Видео и аудио файлы предоставлены, можете скачивать")

    video.close()
    audio.close()
    await state.finish()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял")

executor.start_polling(dp, skip_updates=True)