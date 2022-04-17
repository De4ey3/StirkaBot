from aiogram.dispatcher.filters import state
from aiogram.types import Message
from main import bot, dp
import murkups as mps
from states import Registration

from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import admin_id
from aiogram.dispatcher import FSMContext

import sqlite3

db = sqlite3.connect('pupils.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
tgid BIGINT,
surname TEXT,
name TEXT,
patronymic TEXT,
room INT,
warns INT
)""")

db.commit()


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


@dp.message_handler(commands=['start'])  # Команда /start
async def send_welcome(msg: Message):
    await msg.answer(f'Добрый день, {msg.from_user.first_name}, здесь вы можете записаться на стирку')
    await msg.answer('Для начала вам нужно зарегистрироваться(команда /reg)')


@dp.message_handler(commands=['help'])  # Команда /help
async def get_help(msg: Message):
    await msg.answer('/help - список команд \n'
                     '/free - свободные места \n'
                     '/wash - записаться настирку \n'
                     '/chname - изменить имя \n'
                     '/chroom - изменить комнату \n'
                     '/chbuild - изменить общежитие \n'
                     '/cancel - отменить стирку'
                     )


@dp.message_handler(commands=['reg'])
async def start_reg(msg: Message):
    await msg.answer('Введите ваше ФИО')
    await Registration.waiting_for_name.set()


@dp.message_handler(state=Registration.waiting_for_name)
async def set_name(msg: Message, state: FSMContext):
    if len(msg.text.split()) != 3:
        await msg.answer('Введите корректное имя')
        return
    await state.update_data(tgid=msg.from_user.id)
    await state.update_data(name=msg.text)
    await msg.answer('Теперь введите ваш блок')
    await Registration.next()


@dp.message_handler(state=Registration.waiting_for_room)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(room=msg.text)
    userinfo = await state.get_data()
    await state.finish()
    full_name = userinfo['name'].split()
    surname = full_name[0]
    name = full_name[1]
    patronymic = full_name[2]
    tgid = userinfo['tgid']
    room = userinfo['room']
    sql.execute("SELECT surname FROM users")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (tgid, surname, name, patronymic, room, 0))
        await msg.answer('Отлично, вы прошли регистрацию',
                     reply_markup=mps.startMenu)
    else:
        print('Вы уже зарегистрировались!')


@dp.message_handler(content_types=['text'])  # Команды
async def get_text_messages(msg: Message):
    if "прив" in msg.text.lower():
        await msg.answer('Привет!')
    if "места" in msg.text.lower() or msg.text.lower() == '/free':
        await msg.answer('Google tables: вот таблица с местами')
        # Еще напечатать на ближайший свободный день
    elif "стирк" in msg.text.lower() or msg.text.lower() == '/wash':
        await msg.answer('Вы записаны на стирку')
    elif msg.text.lower() == '/chname':
        await msg.answer('Введите ваше новое имя:')
    elif msg.text.lower() == '/chroom':
        await msg.answer('Введите ваш новый блок:')
    elif msg.text.lower() == '/chbuild':
        await msg.answer('Введите ваше общежитие:')
    else:
        await msg.answer('Неизвестная команда, напишите /help чтобы посмотреть список команд')
