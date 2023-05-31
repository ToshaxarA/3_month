from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from sch_bot import dp
from sql import add_time, add_tsk, show_all_tasks

@dp.message_handler(Command('add_time'))
async def add_cmd(message: Message):
    s = ' '.join(message.text.split(' ')[1:])
    await add(s)
    await message.answer('Запись времени успешно добавлена!')

@dp.message_handler(Command('add_tsk'))
async def add_cmd(message: Message):
    x = ' '.join(message.text.split(' ')[1:])
    await add(x)
    await message.answer('Запись дела успешно добавлена!!!')

@dp.message_handler(Command('show_all_tasks'))
async def buy_cmd(message: Message):
    await message.answer(await show_all_tasks())