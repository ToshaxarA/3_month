from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.message import EmailMessage
import os, logging, requests

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class TextState(StatesGroup):
    choosing_currency = State()
    calculation_usd = State()
    calculation_eur = State()
    calculation_rub = State()
    calculation_kzt = State()
    calculation_som_v_rub = State()


@dp.message_handler(commands='start')
async def start(message:types.Message):
    image_url = 'https://www.akchabar.kg/media/article/money.jpeg.850x445_q82_crop.jpg'

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
    await message.reply(f"""Привет {message.from_user.first_name}! Я информационный бот для конвертации денежных единиц. Чтобы узнать текущий курс НацБанка Кыргызстана введи команду /currency\nДля конвертации Вашей денежной единицы нажмите далее на кнопку той валюты, которую вы хотите конвертировать.""")
                        
@dp.message_handler(commands='currency')
async def get_currency(message:types.Message):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for usd in currency[0:1]:
        usd_currency = usd.text    
    for eur in currency[2:3]:
        eur_currency = eur.text
    for rub in currency[4:5]:
        rub_currency = rub.text
    for kzt in currency[6:7]:
        kzt_currency = kzt.text

    await message.answer(f"""Вот текущие курсы в сомах:
USD:{usd_currency}
EUR:{eur_currency}
RUB:{rub_currency}
KZT:{kzt_currency}

Какую Валюту хотите конвертировать в сомы?""", reply_markup=inline)
    

logging.basicConfig(level=logging.INFO)

inline_keyboards = [
    InlineKeyboardButton ('$ USD 💵 🇺🇸', callback_data='usd'),
    InlineKeyboardButton ('€ EUR 💶 🇪🇺', callback_data='eur'),
    InlineKeyboardButton ('₽ RUB 🇷🇺', callback_data='rub'),
    InlineKeyboardButton ('₸ KZT 🇰🇿', callback_data='kzt'),
    InlineKeyboardButton ('🇰🇬 Сомы в рубли 🇷🇺', callback_data='som_v_rub'),

]
inline = InlineKeyboardMarkup(row_width=4).add(*inline_keyboards)

# Обработчик инлайн кнопок
@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    await TextState.choosing_currency.set()
    if call.data == 'usd':
        await convertion_usd(call.message)
    elif call.data == 'eur':
        await convertion_eur(call.message)
    elif call.data == 'rub':
        await convertion_rub(call.message)
    elif call.data == 'kzt':
        await convertion_kzt(call.message)
    elif call.data == 'som_v_rub':
        await convertion_som_v_rub(call.message)
        
@dp.message_handler(commands='usd')
async def convertion_usd(message:types.Message):
    await message.answer(f"Какую сумму хотите конвертировать?: ")
    await TextState.calculation_usd.set()

@dp.message_handler(state=TextState.calculation_usd)
async def get_subject(message:types.Message, state:FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for usd in currency[0:1]:
        usd_currency = usd.text
        
    await state.update_data(calculation=message.text)
    number = float(message.text)
    kurs_s_tochkoi_usd = float(usd_currency.replace(',','.'))
    itog = round(kurs_s_tochkoi_usd*number, 2)   
    await message.answer(f"В сомах {number} USD будет: {itog}")
    await state.finish()

@dp.message_handler(commands='eur')
async def convertion_eur(message:types.Message):
    await message.answer(f"Какую сумму хотите конвертировать?: ")
    await TextState.calculation_eur.set()

@dp.message_handler(state=TextState.calculation_eur)
async def get_course_eur(message:types.Message, state:FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for eur in currency[2:3]:
        eur_currency = eur.text
        
    await state.update_data(calculation=message.text)
    number = float(message.text)
    kurs_s_tochkoi_eur = float(eur_currency.replace(',','.'))
    itog = round(kurs_s_tochkoi_eur*number,2)  
    await message.answer(f"В сомах {number} Евро будет: {itog}")
    await state.finish()

@dp.message_handler(commands='rub')
async def convertion_rub(message:types.Message):
    await message.answer(f"Какую сумму хотите конвертировать?: ")
    await TextState.calculation_rub.set()

@dp.message_handler(state=TextState.calculation_rub)
async def get_course_rub(message:types.Message, state:FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for rub in currency[4:5]:
        rub_currency = rub.text
        
    await state.update_data(calculation=message.text)
    number = float(message.text)
    kurs_s_tochkoi_rub = float(rub_currency.replace(',','.'))
    itog = round(kurs_s_tochkoi_rub*number, 2)   
    await message.answer(f"В сомах {number} Рублей будет: {itog}")
    await state.finish()

@dp.message_handler(commands='kzt')
async def convertion_kzt(message:types.Message):
    await message.answer(f"Какую сумму хотите конвертировать?: ")
    await TextState.calculation_kzt.set()

@dp.message_handler(state=TextState.calculation_kzt)
async def get_course_kzt(message:types.Message, state:FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for kzt in currency[6:7]:
        kzt_currency = kzt.text
        
    await state.update_data(calculation=message.text)
    number = float(message.text)
    kurs_s_tochkoi_kzt = float(kzt_currency.replace(',','.'))
    itog = round(kurs_s_tochkoi_kzt*number, 2)   
    await message.answer(f"В сомах {number} Тенге будет: {itog}")
    await state.finish()

@dp.message_handler(commands='som_v_rub')
async def convertion_som_v_rub(message:types.Message):
    await message.answer(f"Какую сумму хотите конвертировать?: ")
    await TextState.calculation_som_v_rub.set()

@dp.message_handler(state=TextState.calculation_som_v_rub)
async def get_course_som_v_rub(message:types.Message, state:FSMContext):
    url = 'https://www.nbkr.kg/index.jsp?lang=RUS'
    responce =requests.get(url)
    soup=BeautifulSoup(responce.text, 'lxml')
    currency = soup.find_all('td', class_='exrate')
    for som_v_rub in currency[4:5]:
        som_v_rub_currency = som_v_rub.text
        
    await state.update_data(calculation=message.text)
    number = float(message.text)
    kurs_s_tochkoi_som_v_rub = float(som_v_rub_currency.replace(',','.'))
    
    itog = round((number/kurs_s_tochkoi_som_v_rub), 2)   
    await message.answer(f"В рублях {number} сом будет: {itog}")
    await state.finish()

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял, попробуйте команду /start")

executor.start_polling(dp, skip_updates=True)

