from telebot import types
import bot_funcs as bf
from db_handler import DB_handler as db


# клавиатура выбора процедур
procedures_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
procedures = bf.get_procedures()
procedures.append('Главное меню')
btns = [types.KeyboardButton(procedure) for procedure in procedures]
procedures_keyboard.add(*btns)


# клавиатура админа
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  
btn_texts = ['Посмотреть записи', 'Обновить прайс', 'Скачать шаблон прайса', 
            'Обновить процедуры', 'Скачать шаблон процедур', 'Скачать файл окошек', 'Посмотреть свободные окна'] 
btns = [types.KeyboardButton(text) for text in btn_texts]
admin_keyboard.add(*btns)

# клавиатура главного меню
main_keyboard =  types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_texts = ['Записаться', 'Перенести/отменить визит', 'Проверить запись', 
            'Настроить напоминания', 'Прайс', 'Обо мне', 'Что может бот?']
btns = [types.KeyboardButton(text) for text in btn_texts]
main_keyboard.add(*btns)
