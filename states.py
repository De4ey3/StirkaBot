from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_room = State()
