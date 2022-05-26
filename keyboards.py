from telebot import types
import bot_funcs as bf
from db_handler import db


# клавиатура выбора процедур
procedures_keyboard = types.InlineKeyboardMarkup(row_width=1)
# procedures = db.get_procedures_db()
procedures = db.get_procedures_db()
procedures.append('Главное меню')
btns = [types.InlineKeyboardButton(procedure, callback_data='procedure=' + procedure) for procedure in procedures]
procedures_keyboard.add(*btns)


# клавиатура админа
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  
btn_texts = ['Посмотреть записи', 'Обновить прайс', 'Скачать шаблон прайса', 
            'Обновить процедуры', 'Скачать шаблон процедур', 'Скачать файл окошек', 'Посмотреть свободные окна'] 
btns = [types.KeyboardButton(text) for text in btn_texts]
admin_keyboard.add(*btns)

# клавиатура главного меню
main_keyboard =  types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_texts = ['Записаться', 'Перенести/отменить визит', 'Проверить запись', 
            'Настроить напоминания', 'Прайс', 'Обо мне', 'Что может бот?']
btns = [types.KeyboardButton(text) for text in btn_texts]
main_keyboard.add(*btns)


