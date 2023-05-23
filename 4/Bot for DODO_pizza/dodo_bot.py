from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
import os, logging, sqlite3

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)

inline_keyboards = [ 
    InlineKeyboardButton('Отправить номер', callback_data='phone1'),
    InlineKeyboardButton('Отправить локацию', callback_data='location'),
    InlineKeyboardButton('Заказать еду', callback_data='order')
]
inline_keyboards2 = [ 
    InlineKeyboardButton('Ok', callback_data='1'),
]

inline = InlineKeyboardMarkup().add(*inline_keyboards)
inline2 = InlineKeyboardMarkup().add(*inline_keyboards2)
database = sqlite3.connect('DODO_PIZZA.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id_user INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(150),
    phone VARCHAR(50)
);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    id_user INT,
    address_longitude VARCHAR(150),
    address_latitude VARCHAR(150)
);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    title VARCHAR(255), 
    address_destination VARCHAR(255),
    date_time_order VARCHAR(50)
);
""")
cursor.connection.commit()
logging.basicConfig(level=logging.INFO)

class PushState(StatesGroup):
    phone = State()
    location = State()
    order = State()

# Обработчик инлайн кнопок
@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'phone1':
        await set_phone_user(call.message)


# @dp.callback_query_handler(lambda call: call)
# async def all_inline(call):
#     if call.data == 'phone':
#         await phone_number(call.message)
#     elif call.data == 'location':
#         await mark_location(call.message)
#     elif call.data == 'order':
#         await make_order(call.message)


@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}!", reply_markup=inline)
    cursor=database.cursor()
    cursor.execute(f'SELECT id_user FROM users WHERE id_user = {message.from_user.id};')
    result = cursor.fetchall()

    print(f"'{message.from_user.id}','{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}'")
    
    if result == []:
        cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.id}','{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', 'None');")
    cursor.connection.commit()

@dp.message_handler(commands='set_phone',state=PushState.phone)
async def set_phone_user(message:types.Message, state:FSMContext):
    await message.answer('Введите свой номер телефона')
    await state.update_data(phone = message.text)
    cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.id}','{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', '{message.text}');")
    cursor.connection.commit()
    await message.answer("Телефон записан, спасибо!")
    await PushState.phone.set()
    





    

# @dp.message_handler(commands=['android'])
# async def android(message: types.Message):
#     await message.answer(f'Android-разработчик - это специалист, который занимается созданием приложений и программного обеспечения для операционной системы Android. Он использует язык программирования Java, Kotlin или другие языки, поддерживаемые платформой Android\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
#                         reply_markup=inline)

# @dp.message_handler(text=['/cancel'],)
# async def video_cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply(f'Можете посмотерть другие направление.', reply_markup=keyboard1)

    
# @dp.message_handler(commands=['ios'])
# async def ios(message: types.Message):
#     await message.answer(f'iOS-разработчик - это специалист, который занимается разработкой приложений для устройств, работающих под управлением операционной системы iOS, разработанной компанией Apple. iOS-разработчик использует язык программирования Swift или Objective-C и инструменты разработки, предоставляемые Apple, такие как Xcode и т.д.\nСтоимость 10000 сом в месяц.\nОбучение: 7 месяц',
#                         reply_markup=inline)

# @dp.message_handler(commands=['backend'])
# async def backend(message: types.Message):
#     await message.answer(f'Backend-разработчик - это специалист, который занимается созданием и поддержкой серверной части программного обеспечения. Он отвечает за разработку и поддержку логики, обработку данных и взаимодействие с базами данных \nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
#                         reply_markup=inline)

# @dp.message_handler(commands=['frontend'])
# async def frontend(message: types.Message):
#     await message.answer(f'Frontend-разработчик - это специалист, который занимается разработкой пользовательского интерфейса (UI) веб-приложений. Он отвечает за создание визуальной части приложения, с которой взаимодействует пользователь.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
#                         reply_markup=inline)
    
# @dp.message_handler(commands=['uxui'])
# async def uxui(message: types.Message):
#     await message.answer(f'UX/UI разработчик (User Experience/User Interface) занимается проектированием и разработкой пользовательского интерфейса (UI) и опыта пользователя (UX) для различных цифровых продуктов, таких как мобильные приложения, веб-сайты, программное обеспечение и другие интерактивные системы.\nСтоимость 10000 сом в месяц.\nОбучение: 5 месяц',
#                         reply_markup=inline)

# @dp.message_handler(commands=['sign_up'])
# async def sign_up(message:types.Message):
#     await message.answer("Укажите свои данные")
#     await message.answer("Ваше имя:")
#     await SignUpState.name.set()

# @dp.message_handler(state=SignUpState.name)
# async def get_name(message:types.Message, state:FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Телефонный номер в формате +996:")
#     await SignUpState.tel.set()

# @dp.message_handler(state=SignUpState.tel)
# async def get_number(message:types.Message, state:FSMContext):
#     if len(message.text) == 13 and message.text[1:].isdigit() and message.text[0] == "+":
#         await state.update_data(tel=message.text)
#         await message.answer("Почта:")
#         await SignUpState.email.set()
#     else:
#         await message.answer("Неправильный формат")

# @dp.message_handler(state=SignUpState.email)
# async def get_email(message:types.Message, state:FSMContext):
#     if '@' in message.text:
#         await state.update_data(email=message.text)
#         await message.answer("OK")
#         user_data = await storage.get_data(user=message.from_user.id)
#         print(user_data)
#         t1={time.ctime()}
#         cursor = database.cursor()

#         cursor.execute(f"""INSERT INTO signup VALUES(
#             {message.from_user.id},
#             '{user_data['name']}',
#             '{user_data['tel']}',
#             '{user_data['email']}',
#             '{time.ctime()}'
#         );""")
#         cursor.connection.commit()
#         await message.answer("Ваши данные успешно сохранены")

#         await bot.send_message(chat_id=-947291422,text = f"{user_data['name']}, {user_data['tel']}, {user_data['email']}, {t1}")
#     else:
#         await message.answer("Неправильная почта")



executor.start_polling(dp, skip_updates=True)