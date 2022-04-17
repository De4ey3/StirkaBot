import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
import murkups as mps

loop = asyncio.get_event_loop()# Токен бота
bot = Bot(BOT_TOKEN, parse_mode='HTML') # Обозначаем бота, прописываем токен и формат текста HTML
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop) # Диспетчер для бота

# Запуск бота
if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True) # Пропускаем обновления