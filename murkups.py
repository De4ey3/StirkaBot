from aiogram.types import ReplyKeyboardMarkup as rkm, KeyboardButton as kb

# --- Start Menu ---
btnWash = kb('Записаться на стирку')
btnFreePlace = kb('Посмотреть свободные места')
startMenu = rkm(resize_keyboard=True).add(btnWash, btnFreePlace)


