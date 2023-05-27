file_name = input("Имя файла: ")
with open(f'{file_name}', 'w', encoding='utf-8') as python_script:
    python_script.write("""from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, aioschedule, requests, logging

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

executor.start_polling(dp, skip_updates=True)
    """)