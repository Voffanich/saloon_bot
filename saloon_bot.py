import threading
from datetime import datetime as dt
from datetime import timedelta

import telebot
from telebot import types

import bot_funcs as bf
import g_funcs as gf
import keyboards as kb
import ru_dates as rd
import user_data.messages as msg
from client import Client
from credentials import admin_ids, admin_usernames, apikey
from db_handler import db

cfg_general = bf.read_config('config.json')['general']

# Бэкап файла БД при рестарте бота
db.backup_db_file(cfg_general['db_file_name'], 'bot_restart')

# Создание потока с задачами по расписанию, без daemon = True поток продолжает работу после завершения работы основного скрипта
sсheduled_tasks_thread = threading.Thread(target = bf.scheduled_tasks, 
                                          kwargs = {'db_file_name':cfg_general['db_file_name'],
                                                    'days_to_store_backups':cfg_general['days_to_store_db_backups'], 
                                                    'calendar_id':gf.calendar_id_2,
                                                    'days_to_show_windows':cfg_general['days_to_show_booktimes'],
                                                    'mins_to_occupy_window':cfg_general['mins_to_occupy_window'],
                                                    'window_colors':cfg_general['window_colors']}, daemon = True)

bot = telebot.TeleBot(apikey)

clients = bf.create_client_objects_from_db()
procedures = db.get_procedures_data()

# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(message, res=False):
    if message.from_user.id not in clients:
        clients[message.from_user.id] = Client(message.from_user.id, '', '', '', '', '')
        bot.send_message(message.chat.id, text=msg.UNKNOWN_WELCOME, 
                                        reply_markup=kb.main_keyboard)
    else:    
        bot.send_message(message.chat.id, 
                text=msg.KNOWN_WELCOME, 
                reply_markup=kb.main_keyboard)
           
# @bot.message_handler(func=lambda message: clients[message.from_user.id].flag == 'проверить телефон')
@bot.message_handler(func=lambda message: bf.check_flag(clients, message.from_user.id) == 'проверить телефон')
def verify_phone_number(message):
    if bf.validate_phone(message.text)[0]:
       
        clients[message.from_user.id].phone_number = bf.validate_phone(message.text)[1]    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Телефон верный")
        btn2 = types.KeyboardButton("Изменить номер телефона")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 
                text=f'Номер телефона <b>{clients[message.from_user.id].phone_number}</b> верный?', 
                parse_mode='HTML', reply_markup=markup)
        clients[message.from_user.id].flag = '' 
    else:
        bot.send_message(message.chat.id, text='Вы ввели некорректный номер телефона. Введите, пожалуйста, правильный в формате +375хх без пробелов и дефисов')

# @bot.message_handler(func=lambda message: clients[message.from_user.id].flag == 'проверить имя')
@bot.message_handler(func=lambda message: bf.check_flag(clients, message.from_user.id) == 'проверить имя')
def verify_name(message):
    if bf.validate_name(message.text)[0]:
        clients[message.from_user.id].first_name = bf.validate_name(message.text)[1]
        clients[message.from_user.id].last_name = bf.validate_name(message.text)[2]
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Да, имя верное")
        btn2 = types.KeyboardButton("Изменить имя")
        clients[message.from_user.id].flag = ''
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Записываем вас под именем <b>{clients[message.from_user.id].first_name} {clients[message.from_user.id].last_name}</b>?', reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, text=f'Вы ввели некорректное имя. Введите, пожалуйста, имя и фамилия в формате <b>Имя Фамилия</b>', parse_mode="HTML")
        clients[message.from_user.id].flag = 'проверить имя'
    
@bot.message_handler(content_types=['text'])
def func(message):
    
    
    if (message.text == 'Что может бот?'):
        bot.send_message(message.chat.id, text=msg.BOT_CAN_DO,
                         reply_markup=kb.main_keyboard)
            
    
    elif (message.text == 'Записаться'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        # clients[message.from_user.id].username = message.from_user.username
        # clients[message.from_user.id].first_name = message.from_user.first_name
        # clients[message.from_user.id].last_name = message.from_user.last_name
                
        if db.client_exists(message.from_user.id):
            bot.send_message(message.chat.id, text=msg.PROCEDURES_COMMENT, reply_markup=kb.procedures_keyboard)
        else:
            btn1 = types.KeyboardButton("Оставляем")
            btn2 = types.KeyboardButton("Изменить имя")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text='Вы не знакомы боту) Давайте-ка занесем вас в базу клиентов. '
                                                    f'В телеграме вы подписаны как <b>{message.from_user.first_name} {message.from_user.last_name}</b>. '
                                                    'Оставляем или хотите изменить?', reply_markup=markup, parse_mode="HTML")
    
                    
    elif (message.text == 'Перенести/отменить визит'):
        bot.send_message(message.chat.id, text='Ну, начинается!')
        
        
    elif (message.text == 'Проверить запись'):
        bot.send_message(message.chat.id, text='Вы записаны тогда-то на столько-то')
        
        
    elif (message.text == 'Настроить напоминания'):
        bot.send_message(message.chat.id, text='Включите, выключите, настройте время напоминания о визите')
        
        
    elif (message.text == 'Прайс'):
        bot.send_message(message.chat.id, text='Скоро добавим)', reply_markup=kb.main_keyboard)
        
        
    elif (message.text == 'Обо мне'):
        bot.send_message(message.chat.id, text=msg.ABOUT, reply_markup=kb.main_keyboard)
    
    
    elif (message.text == 'Как добраться'):
        bot.send_message(message.chat.id, text=msg.LOCATION, reply_markup=kb.main_keyboard, parse_mode='HTML')
    
    
    elif (message.text == 'Написать мастеру'):
        bot.send_message(message.chat.id, text=msg.TG_CONTACT, reply_markup=kb.main_keyboard, parse_mode='HTML')    
        
        
    elif (message.text == 'Оставляем'):
        clients[message.from_user.id].first_name = message.from_user.first_name
        clients[message.from_user.id].last_name = message.from_user.last_name
        bot.send_message(message.chat.id, text='Хорошо. Теперь введите ваш номер телефона в формате +375хх без пробелов и дефисов', reply_markup='')
        clients[message.from_user.id].flag = 'проверить телефон'        
        
        
    elif (message.text == 'Изменить имя'):
        bot.send_message(message.chat.id, text='Введите, пожалуйста, ваши имя и фамилию в формате <b>Имя Фамилия</b>. Желательно записаться по реальному имени и фамилии. Фамилию можно просто одной буквой с точкой написать (например Юлия М.)', parse_mode='HTML')
        clients[message.from_user.id].flag = 'проверить имя' 
    
    
    elif (message.text == 'Изменить номер телефона'):
        bot.send_message(message.chat.id, text='введите ваш номер телефона в формате +375хх без пробелов и дефисов')
        clients[message.from_user.id].flag = 'проверить телефон' 
    
    
    elif (message.text == 'Да, имя верное'):
        bot.send_message(message.chat.id, text='Чудненько! Теперь введите ваш номер телефона в формате +375хх без пробелов и дефисов', reply_markup='')
        clients[message.from_user.id].flag = 'проверить телефон'
    
    
    elif (message.text == 'Телефон верный'):
        bot.send_message(message.chat.id, text=f'Чудненько, сохранили вас в базе клиентов как <b>{clients[message.from_user.id].first_name} {clients[message.from_user.id].last_name}, {clients[message.from_user.id].phone_number}</b>. Теперь можете выбрать процедуру, на которую хотели бы прийти', reply_markup=kb.procedures_keyboard, parse_mode='HTML')
        db.add_client(message.from_user.id, message.from_user.username, clients[message.from_user.id].first_name, clients[message.from_user.id].last_name, clients[message.from_user.id].phone_number)        
        clients[message.from_user.id].flag = 'выбор процедуры'
        
        
    elif (message.text.lower() == 'admino' or message.text.lower() == 'админо'):                
        if message.from_user.username in admin_usernames:
            bot.send_message(message.chat.id, text='Привет, админ!', reply_markup=kb.admin_keyboard)
            clients[message.from_user.id].admin = True
        else:
            bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота', reply_markup=kb.main_keyboard)
    
    
    elif (message.text.lower() == 'admino stop' or message.text.lower() == 'stop admino' or message.text.lower() == 'админо стоп' or message.text.lower() == 'стоп админо'):
        clients[message.from_user.id].admin = False      
        bot.send_message(message.chat.id, text='admin mode off', reply_markup=kb.main_keyboard)
    
    elif (message.text == 'Показать статистику'):
        bot.send_message(message.chat.id, text='Выберите месяц для отображения статистики', reply_markup=kb.main_stats_keyboard) 
         
    elif (message.text == 'Выгрузить окна'):
        bot.send_message(message.chat.id, text='Выберите месяц для отображения свободных для записи окон', reply_markup=kb.main_windows_keyboard) 
            
    else:
        bot.send_message(message.chat.id, text=msg.UNKNOWN_COMMAND)

@bot.callback_query_handler(func=lambda call: True)
def func(call):
    # вывод доступных для посещения дней для выбранной процедуры
    if 'procedure_id=' in call.data:
        procedure_id = int(call.data.split('=')[1])
        clients[call.from_user.id].chosen_procedure_id = procedure_id
        procedure_name = procedures[procedure_id - 1]['procedure']
        # dates = bf.get_available_times(procedures, procedure_id, cfg_general['days_to_show_booktimes'],
        #                                                          cfg_general['mins_to_nearest_book'])
        dates = gf.clndr.get_available_times(gf.calendar_id_2, cfg_general['days_to_show_booktimes'], 
                                                                 cfg_general['mins_to_nearest_book'])
        dates_keyboard = kb.create_dates_keyboard(dates)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=f'Выберите день, на который можно записаться на <b>{procedure_name}</b>', 
                              reply_markup=dates_keyboard, parse_mode='HTML')
    
    # вывод доступных для посещения процедур    
    elif call.data == 'choose_procedure':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg.PROCEDURES_COMMENT, reply_markup=kb.procedures_keyboard)
    
    # возврат в главное меню бота
    elif call.data == 'Главное меню':
        bot.send_message(chat_id=call.message.chat.id, text='Главное меню', reply_markup=kb.main_keyboard)
    
    # вывод доступных для записи времен (окон)    
    elif call.data.startswith('day='):
        day = call.data.split('=')[1]  
        procedure_id = clients[call.from_user.id].chosen_procedure_id
        # dates = bf.get_available_times(procedures, procedure_id, cfg_general['days_to_show_booktimes'],
        #                                                                  cfg_general['mins_to_nearest_book'])     
        dates = gf.clndr.get_available_times(gf.calendar_id_2, cfg_general['days_to_show_booktimes'], 
                                                                 cfg_general['mins_to_nearest_book'])
        times_keyboard = kb.create_times_keyboard(dates, day, clients[call.from_user.id].chosen_procedure_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите подходящее время из доступных на <b>' + day + '</b>', reply_markup=times_keyboard, parse_mode='HTML')
    
    # подтверждение записи на выбранное время
    elif call.data.startswith('daytime&'):
        book_date_ru = call.data.split('&')[1]
        book_time = call.data.split('&')[2]
        procedure_id = clients[call.from_user.id].chosen_procedure_id
        procedure_duration = procedures[procedure_id - 1]['duration'] 
        procedure_name = procedures[procedure_id - 1]['procedure']
        booked_date_ru = book_date_ru + '&' + book_time
        
        print(f'{book_date_ru=}\n{book_time=}')
        
        # booked_date = dt.strptime(dt.strftime(rd.date_from_ru_weekday_comma_date(book_date_ru), '%Y-%m-%d') + book_time, '%Y-%m-%d%H:%M')
        booked_date = dt.strptime(f'{dt.now().year}-{book_date_ru.split(",")[0]}' + book_time, '%Y-%d.%m%H:%M') 
        
        if booked_date < dt.now():
            book_date += timedelta(years=1) 
        
        
        
        # if bf.window_occupied(booked_date, procedure_duration, cfg_general['days_to_show_booktimes']):
        if not gf.clndr.check_window_occupation(gf.calendar_id_2, booked_date, call.from_user.id):
            mess_text = f'К сожалению, на это время кто-то уже успел записаться. Посмотрите, пожалуйста, другие варианты'
            # dates = bf.get_available_times(procedures, procedure_id, cfg_general['days_to_show_booktimes'],
            #                                                      cfg_general['mins_to_nearest_book'])
            dates = gf.clndr.get_available_times(gf.calendar_id_2, cfg_general['days_to_show_booktimes'], 
                                                                 cfg_general['mins_to_nearest_book'])
            dates_keyboard = kb.create_dates_keyboard(dates)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text, reply_markup=dates_keyboard, parse_mode='HTML')
        else:  
            if gf.clndr.occupy_window(gf.calendar_id_2, booked_date, call.from_user.id, cfg_general['window_colors']): 
                mess_text = f'Записываю вас на <b>{procedure_name}</b> на <b>{book_date_ru}, {book_time}</b>?'
                confirm_book_keyboard = kb.create_confirm_book_keyboard(procedures, procedure_id, booked_date_ru)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text, reply_markup=confirm_book_keyboard, parse_mode='HTML') 
            
            else:
                mess_text = f'К сожалению, на это время кто-то уже успел записаться. Посмотрите, пожалуйста, другие варианты'
                # dates = bf.get_available_times(procedures, procedure_id, cfg_general['days_to_show_booktimes'],
                #                                                      cfg_general['mins_to_nearest_book'])
                dates = gf.clndr.get_available_times(gf.calendar_id_2, cfg_general['days_to_show_booktimes'], 
                                                                    cfg_general['mins_to_nearest_book'])
                dates_keyboard = kb.create_dates_keyboard(dates)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text, reply_markup=dates_keyboard, parse_mode='HTML')
    
    # занесение записи на процедуру в базу
    elif call.data.startswith('confirm_book&'):
        procedure_id = int(call.data.split('&')[1])
        
        # book date for message
        ru_visit_date = call.data.split('&')[2]
        print(f'{ru_visit_date=}')
        # book time for message
        book_time = call.data.split('&')[3]
        # db_book_date = dt.strftime(rd.date_from_ru_weekday_comma_date(book_date_ru), '%Y-%m-%d')
        duration = procedures[procedure_id - 1]['duration']
        # procedure duration as timedelta object
        procedure_duration = timedelta(hours = int(duration.split(':')[0]), minutes = int(duration.split(':')[1]))  
        
        year = dt.now().year
                
        # start_time = dt.strftime(rd.date_from_ru_weekday_comma_date(ru_visit_date), '%Y-%m-%d') + ' ' + call.data.split('&')[3] # str
        start_time = f'{year}.{ru_visit_date.split(",")[0]}' + ' ' + call.data.split('&')[3] # str
        
        if dt.strptime(f'{start_time}', '%Y.%d.%m %H:%M') < dt.now():
            year += 1
            start_time = f'{year}.{ru_visit_date.split(",")[0]}' + ' ' + call.data.split('&')[3] # str
           
        finish_time = dt.strftime(dt.strptime(start_time, '%Y.%d.%m  %H:%M') +  procedure_duration, '%Y-%m-%d %H:%M') #str
        
        book_date = dt.strftime(dt.now(), '%Y-%m-%d %H:%M')
                 
        procedure = procedures[procedure_id -1]['procedure']
        # procedure = bf.procedure_name_from_id(procedures, procedure_id)
        
        # client_name = clients[call.from_user.id].first_name or '' + ' ' +  clients[call.from_user.id].last_name or ''
        client_name = clients[call.from_user.id].first_name + ' ' +  clients[call.from_user.id].last_name or ''
        phone_number = clients[call.from_user.id].phone_number
       
        price = int(procedures[procedure_id - 1]['price'])
        
        # booked_date = dt.strptime(dt.strftime(rd.date_from_ru_weekday_comma_date(ru_visit_date), '%Y-%m-%d') + book_time, '%Y-%m-%d%H:%M')
        booked_date = dt.strptime(start_time, '%Y.%d.%m %H:%M')
        start_time = dt.strftime(booked_date, '%Y-%m-%d %H:%M')
        
        proc_duration_str = procedures[procedure_id - 1]['duration'] 
        
        if not gf.clndr.check_window_occupation(gf.calendar_id_2, booked_date, call.from_user.id):
            mess_text = f'К сожалению, на это время кто-то уже успел записаться. Возможно, вы слишком долго подтверждали запись'
            # dates = bf.get_available_times(procedures, procedure_id, cfg_general['days_to_show_booktimes'],
            #                                                      cfg_general['mins_to_nearest_book'])
            dates = gf.clndr.get_available_times(gf.calendar_id_2, cfg_general['days_to_show_booktimes'], 
                                                                 cfg_general['mins_to_nearest_book'])
            dates_keyboard = kb.create_dates_keyboard(dates)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text, reply_markup=dates_keyboard, parse_mode='HTML')
        else:
            mess_text = f'Отлично, вы записаны на <b>{procedure}</b> на <b>{ru_visit_date}, {book_time}</b>'
            db.add_visit(client_name, book_date, ru_visit_date, start_time, finish_time, procedure_id, 'active', price)
            gf.clndr.add_visit(gf.calendar_id_2, booked_date, call.from_user, procedure_id, client_name, phone_number, price, cfg_general['window_colors'])
            # db.show_visits()
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=mess_text, reply_markup='', parse_mode='HTML')
            bot.send_message(chat_id=call.message.chat.id, text='Главное меню', reply_markup=kb.main_keyboard)
    
            for admin_id in admin_ids:
                bot.send_message(chat_id=admin_id, text=f'{client_name} записался на {db.procedure_name_from_id(procedure_id)} на {booked_date}')
    
    # подготовка и вывод статистика за выбранный месяц
    elif call.data.startswith('stats_shift='):
        month_shift = int(call.data.split('=')[1])
        mess_text = gf.clndr.show_stats(calendar_id=gf.calendar_id_2, month_shift=month_shift)
        bot.send_message(chat_id=call.message.chat.id, text=mess_text, reply_markup=kb.admin_keyboard, parse_mode='HTML')
      
    elif call.data.startswith('windows_shift='):    
        month_shift = int(call.data.split('=')[1])
        mess_text = gf.clndr.show_windows(calendar_id=gf.calendar_id_2, month_shift=month_shift)
        bot.send_message(chat_id=call.message.chat.id, text=mess_text, reply_markup=kb.admin_keyboard, parse_mode='HTML')
        
# Запуск бота    
# bot.polling(non_stop = True, interval = 0, timeout=0) # изучить параметры timeout! non_stop или none_stop?

if __name__ == '__main__':
    sсheduled_tasks_thread.start()
    # try:
    #     bot.polling(non_stop = True, interval = 0, timeout = 0)
    # except:
    #     pass
    bot.infinity_polling()
    
    
    # .\venv\scripts\activate.ps1 
    # terminal docker bot run command
    # docker run -e PYTHONUNBUFFERED=1 --restart=unless-stopped -d saloon_bot