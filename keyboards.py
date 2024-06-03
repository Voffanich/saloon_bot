from telebot import types

import bot_funcs as bf
from db_handler import db

# клавиатура выбора процедур
procedures_keyboard = types.InlineKeyboardMarkup(row_width=1)
# procedures = db.get_procedures_db()
procedures = db.get_procedures_db()
procedures_list = db.get_procedures_data()
btns = [types.InlineKeyboardButton(procedure, callback_data=f'procedure_id={bf.procedure_id_from_name(procedures_list, procedure)}') for procedure in procedures]
btns.append(types.InlineKeyboardButton('Главное меню', callback_data='Главное меню'))
procedures_keyboard.add(*btns)


# клавиатура админа
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  
btn_texts = ['Показать статистику', 'Выгрузить окна', 'Обновить прайс', 'Скачать шаблон прайса', 
            'Обновить процедуры', 'Скачать шаблон процедур', 'Скачать файл окошек', 'Удалить из базы В'] 
btns = [types.KeyboardButton(text) for text in btn_texts]
admin_keyboard.add(*btns)

# клавиатура главного меню
main_keyboard =  types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_texts = ['Записаться', 'Мои записи', 'Отменить запись', 'Прайс', 'Обо мне', 'Как добраться', 'Что может бот?', 'Написать мастеру']
# btn_texts = ['Записаться', 'Перенести/отменить визит', 'Проверить запись', 
#             'Настроить напоминания', 'Прайс', 'Обо мне', 'Как добраться', 'Что может бот?']
btns = [types.KeyboardButton(text) for text in btn_texts]
main_keyboard.add(*btns)

# клавиатура выбора месяца, для которого нужно вывести статистику
main_stats_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Предыдущий', callback_data=f'stats_shift=-1')
btn2 = types.InlineKeyboardButton('Текущий', callback_data=f'stats_shift=0')
btn3 = types.InlineKeyboardButton('Следующий', callback_data=f'stats_shift=1')
main_stats_keyboard.add(btn1, btn2, btn3)

# клавиатура выбора месяца, для которого нужно вывести свободные для записи окна
main_windows_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Текущий', callback_data=f'windows_shift=0')
btn2 = types.InlineKeyboardButton('Следующий', callback_data=f'windows_shift=1')
main_windows_keyboard.add(btn1, btn2)

# клавиатура подтверждения записи на выбранную дату и время
def create_confirm_book_keyboard(procedures: list, procedure_id: int, booked_date: str) -> types.InlineKeyboardMarkup:
    book_date = booked_date.split('&')[0]
    book_time = booked_date.split('&')[1]
    
    confirm_book_keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Подтверждаю запись', callback_data=f'confirm_book&{str(procedure_id)}&{book_date}&{book_time}')
    btn2 = types.InlineKeyboardButton('Выбрать другое время', callback_data=f'procedure_id={procedure_id}')
    confirm_book_keyboard.add(btn1, btn2)
    
    return confirm_book_keyboard

# клавиатура, выводящие достуаные времена для записи в выбранный день
def create_times_keyboard(dates: dict, day: str, procedure_id: int)  -> types.InlineKeyboardMarkup:  
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
        btns.append(types.InlineKeyboardButton(time, callback_data = f'daytime&{day}&{time}'))
        
    btns.append(types.InlineKeyboardButton('Выбрать другой день', callback_data=f'procedure_id={procedure_id}'))
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
        btns.append(types.InlineKeyboardButton(f'{day} ({str(len(times))})', callback_data = f'day={day}'))
    
    btns.append(types.InlineKeyboardButton('Выбор процедуры', callback_data='choose_procedure'))    
    proc_slice = slice(0, len(btns)-1, 1)
    dates_keyboard.add(*btns[proc_slice])
    dates_keyboard.row(btns[-1])              
    
    return dates_keyboard

    
def  create_cancel_booking_keyboard(booking_id: str, count: int) -> types.InlineKeyboardMarkup:
    cancel_booking_keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'Отменить запись {count}', callback_data=f'c={booking_id}')
    cancel_booking_keyboard.add(btn1)
    
    return cancel_booking_keyboard

def create_confirm_cancel_booking_keyboard(call_data: str) -> types.InlineKeyboardMarkup:
    booking_id = call_data.replace('c=', '')
    
    confirm_cancel_booking_keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'Не отменять', callback_data=f'd={booking_id}')
    btn2 = types.InlineKeyboardButton(f'Отменить запись', callback_data=f'k={booking_id}')
    confirm_cancel_booking_keyboard.add(btn1, btn2)
    
    return confirm_cancel_booking_keyboard
