from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from les_5 import send_mail, is_valid_email
from dotenv import load_dotenv
from email.message import EmailMessage
import os, logging, requests


load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_keyboards = [
    InlineKeyboardButton('Отправить сообщение', callback_data='send_mail')
]

inline = InlineKeyboardMarkup().add(*inline_keyboards)

class EmailState(StatesGroup):
    mail = State()
    subject = State()
    message = State()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    image_url = 'https://i.siteapi.org/iHOsi9j5J48PBvM56IF9GOB-Abs=/fit-in/330x/top/s.siteapi.org/2b1e774b7a61686/img/pum0ae0azv4848osck4cg0owgsg8wo'

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
    await message.answer(f"Привет {message.from_user.first_name}! Я почтовый YANDEX бот, умею отправлять сообщения.", reply_markup=inline)

@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'send_mail':
        await send_bot_mail(call.message)

@dp.message_handler(commands='send')
async def send_bot_mail(message:types.Message):
    await message.answer("Электронная почта адресата:")
    await EmailState.mail.set()

@dp.message_handler(state=EmailState.mail)
async def get_subject(message:types.Message, state:FSMContext):
    await state.update_data(mail=message.text)
    await message.answer("Введите заголовок:")
    await EmailState.subject.set()

@dp.message_handler(state=EmailState.subject)
async def get_message(message:types.Message, state:FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Введите текст Вашего сообщения:")
    await EmailState.message.set()


@dp.message_handler(state=EmailState.message)
async def send_message(message:types.Message, state:FSMContext):
    
    await state.update_data(text=message.text)
    res = await storage.get_data(user=message.from_user.id)
        
    if is_valid_email(res['mail']):
        await message.answer("Адрес электронной почты введен верно.")
    else:
        await message.answer("Некорректный адрес электронной почты!")

    if is_valid_email(res['mail']) and len(res['text']) < 255:
        await message.answer(f"Количество символов в письме = {len(res['text'])} и не превышает допустимого (255)")
        await message.answer("Отправляем письмо...")
        if send_mail(res['text'], res['subject'], res['mail']):
            
            await message.answer("Письмо отправлено!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Что-то пошло не так... Письмо не отправлено... Не забывайте, что символов в письме не должно быть больше 255. Краткость - сестра таланта!) Попробуете ещё раз?"
                                    , reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await start(message)

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я Вас не понял, попробуйте команду /start")
    
executor.start_polling(dp, skip_updates=True)