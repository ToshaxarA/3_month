from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, aioschedule, requests, logging, asyncio

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

async def send_message():
    await bot.send_message(-947291422, "Hello Geeks")

async def schedule():
    aioschedule.every(0.5).seconds.do(send_message) 
    while True:
        await aioschedule.run_pending()

async def on_startup(hello):
    asyncio.create_task(schedule())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)