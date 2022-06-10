import sys
from telebot import types
import bot_funcs as bf
from db_handler import db


# клавиатура выбора процедур
procedures_keyboard = types.InlineKeyboardMarkup(row_width=1)
# procedures = db.get_procedures_db()
procedures = db.get_procedures_db()
btns = [types.InlineKeyboardButton(procedure, callback_data='procedure=' + procedure) for procedure in procedures]
btns.append(types.InlineKeyboardButton('Главное меню', callback_data='Главное меню'))
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
            'Настроить напоминания', 'Прайс', 'Обо мне', 'Как добраться', 'Что может бот?']
btns = [types.KeyboardButton(text) for text in btn_texts]
main_keyboard.add(*btns)

# клавиатура подтверждения записи на выбранную дату и время
def create_confirm_book_keyboard(procedures: list, procedure: str, booked_date: str) -> types.InlineKeyboardMarkup:
    book_date = booked_date.split('&')[0]
    book_time = booked_date.split('&')[1]
    procedure_id = bf.procedure_id_from_name(procedures, procedure)
    
    confirm_book_keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Подтверждаю запись', callback_data='confirm_book&' + str(procedure_id) + '&' + book_date + '&' + book_time)
    btn2 = types.InlineKeyboardButton('Выбрать другое время', callback_data='procedure=' + procedure)
    confirm_book_keyboard.add(btn1, btn2)
    
    return confirm_book_keyboard

# клавиатура, выводящие достуаные времена для записи в выбранный день
def create_times_keyboard(dates: dict, day: str, procedure: str)  -> types.InlineKeyboardMarkup:  
    """    
    Function creates keyboard with available times for booking.
    
    Args:
        dates (dict): dictionary of available days and times for booking
        day (str): day with available times choosen by user
        procedure (str): chosen procedure
        
    Returns:
        telegram inline keyboard: configured telegram inline keyboard with available days for a chosen procedure
    """
    btns = []
    times_keyboard = types.InlineKeyboardMarkup(row_width=5)
    
    for time in dates[day]:        
        btns.append(types.InlineKeyboardButton(time, callback_data = 'daytime&' + day + '&' + time))
        
    btns.append(types.InlineKeyboardButton('Выбрать другой день', callback_data='procedure=' + procedure))
    proc_slice = slice(0, len(btns)-1, 1)   # создание среза из списка кнопок, все кнопки кроме последней
    times_keyboard.add(*btns[proc_slice])   # добавление самовыравнивающейся клавиатуры из времен, кроме последней кнопки
    times_keyboard.row(btns[-1])            # добавление отдельным рядом кнопки "вернуться к выбору дня"
    
    return times_keyboard


def create_dates_keyboard(dates: dict) -> types.InlineKeyboardMarkup:
    """
    Function creates telegram inline keyboard with with days that have times available for booking.
    
    Args:
        dates (dict): dictionary of available days and times for booking 

    Returns:
        telegram inline keyboard: configured telegram inline keyboard with available times within a chosen day
    """
    btns = []
    dates_keyboard = types.InlineKeyboardMarkup(row_width=3)
    
    for day, times in dates.items():
        btns.append(types.InlineKeyboardButton(day + ' (' + str(len(times)) + ')', callback_data = 'day=' + day))
    
    btns.append(types.InlineKeyboardButton('Выбор процедуры', callback_data='choose_procedure'))    
    proc_slice = slice(0, len(btns)-1, 1)
    dates_keyboard.add(*btns[proc_slice])
    dates_keyboard.row(btns[-1])              
    
    return dates_keyboard