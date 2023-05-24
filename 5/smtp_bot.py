from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging 


load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.INFO)

inline_keyboards = [
    InlineKeyboardButton ('Отправить сообщение', callback_data='send_mail')
]
inline = InlineKeyboardMarkup().add(*inline_keyboards)

class EmailState(StatesGroup):
    mail = State()
    subject = State()
    message = State()


@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hello world!", reply_markup=inline)

# Обработчик инлайн кнопок
@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'send_mail':
        await send_bot_mail(call.message)

@dp.message_handler(commands='send')
async def send_bot_mail(message:types.Message):
    await message.answer("Почта: ")
    await EmailState.mail.set()

@dp.message_handler(state=EmailState.mail)
async def get_subject(message:types.Message, state:FSMContext):
    await state.update_data(mail=message.text)
    await message.answer("Введите заголовок: ")
    await EmailState.subject.set()

@dp.message_handler(state=EmailState.subject)
async def get_message(message:types.Message, state:FSMContext):
    await state.update_data(subject=message.text)
    await message.answer("Введите cообщение: ")
    await EmailState.message.set()

@dp.message_handler(state=EmailState.message)
async def send_message(message:types.Message, state:FSMContext):
    await message.answer("Отправляем письмо...")
    await state.update_data(text=message.text)
    res = await storage.get_data(user=message.from_user.id)
    if send_mail(res['text'], res['subject'], res['mail']):
        await message.answer("Письмо отправлено!", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Что-то пошло не так... Письмо не отправлено. Попробуете ещё раз?"
                                 , reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await start(message)

executor.start_polling(dp, skip_updates=True)

