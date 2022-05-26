
from types import NoneType
import telebot
from telebot import types
from credentials import apikey, admin_usernames
import bot_funcs as bf
from db_handler import db
import keyboards as kb
from client import Client

bot = telebot.TeleBot(apikey)

clients = bf.create_client_objects_from_db()

"""# список клиентов из базы
clients_list = db.clients_list()

# генерация списка объектов клиентов
for clients[message.from_user.id] in clients_list:
    client_objects.append(Clients(clients[message.from_user.id]))"""


# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(message, res=False):
    if message.from_user.id not in clients:
        bot.send_message(message.chat.id, text="Да вы, батенька, впервые тут", reply_markup=kb.main_keyboard)
        clients[message.from_user.id] = Client(message.from_user.id, '', '', '', '', '')
    else:    
        bot.send_message(message.chat.id, text="Дорова! Здесь ты можешь записаться ко мне на процедуры. Жамкай нужные кнопки", reply_markup=kb.main_keyboard)
           
@bot.message_handler(func=lambda message: clients[message.from_user.id].flag == 'проверить телефон')
def verify_phone_number(message):
    if bf.validate_phone(message.text)[0]:
       
        clients[message.from_user.id].phone_number = bf.validate_phone(message.text)[1]    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Телефон верный")
        btn2 = types.KeyboardButton("Изменить номер телефона")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Номер телефона <b>{clients[message.from_user.id].phone_number}</b> верный?', parse_mode='HTML', reply_markup=markup)
        clients[message.from_user.id].flag = '' 
    else:
        bot.send_message(message.chat.id, text='Вы ввели некорректный номер телефона. Введите, пожалуйста, правильный в формате +375хх без пробелов и дефисов')

@bot.message_handler(func=lambda message: clients[message.from_user.id].flag == 'проверить имя')
def verify_name(message):
    if bf.validate_name(message.text)[0]:
        clients[message.from_user.id].first_name = bf.validate_name(message.text)[1]
        clients[message.from_user.id].last_name = bf.validate_name(message.text)[2]
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
        bot.send_message(message.chat.id, text='1. Записаться на процедуру\n2. Посмотреть дату и время записи\n3. Настроить напоминания о визите\n4. Перенести визит\n')
            
    
    elif (message.text == 'Записаться'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        clients[message.from_user.id].username = message.from_user.username
        clients[message.from_user.id].first_name = message.from_user.first_name
        clients[message.from_user.id].last_name = message.from_user.last_name
                
        if db.client_exists(clients[message.from_user.id].username):
            bot.send_message(message.chat.id, text='Такс, выбрайте процедуру, на которую хотите прийти', reply_markup=kb.procedures_keyboard)
        else:
            btn1 = types.KeyboardButton("Оставляем")
            btn2 = types.KeyboardButton("Изменить имя")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text='Впервые здесь? Давайте-ка занесем вас в базу клиентов. '
                                                    f'В телеграме вы подписаны как <b>{clients[message.from_user.id].first_name} {clients[message.from_user.id].last_name}</b>. '
                                                    'Оставляем или хотите изменить?', reply_markup=markup, parse_mode="HTML")
                    
    elif (message.text == 'Перенести/отменить визит'):
        bot.send_message(message.chat.id, text='Ну, начинается!')
        
        
    elif (message.text == 'Проверить запись'):
        bot.send_message(message.chat.id, text='Вы записаны тогда-то на столько-то')
        
        
    elif (message.text == 'Настроить напоминания'):
        bot.send_message(message.chat.id, text='Включите, выключите, настройте время напоминания о визите')
        
        
    elif (message.text == 'Прайс'):
        bot.send_message(message.chat.id, text='Тебе кабзда')
        
        
    elif (message.text == 'Обо мне'):
        bot.send_message(message.chat.id, text='Пушка-гонка-ракета')
        
        
    elif (message.text == 'Оставляем'):
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
        db.add_client(message.from_user.id, clients[message.from_user.id].username, clients[message.from_user.id].first_name, clients[message.from_user.id].last_name, clients[message.from_user.id].phone_number)        
        clients[message.from_user.id].flag = 'выбор процедуры'
        
        
    elif (message.text == 'admino' or message.text == 'админо'):                
        if message.from_user.username in admin_usernames:
            bot.send_message(message.chat.id, text='Привет, админ!', reply_markup=kb.admin_keyboard)
            clients[message.from_user.id].admin = True
        else:
            bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота', reply_markup=kb.main_keyboard)
    
    
    elif (message.text == 'admino stop' or message.text == 'stop admino' or message.text == 'админо стоп' or message.text == 'стоп админо'):
        clients[message.from_user.id].admin = False      
        bot.send_message(message.chat.id, text='admin mode off', reply_markup=kb.main_keyboard)
     
            
    else:
        bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота')

@bot.callback_query_handler(func=lambda call: True)
def func(call):
    if 'procedure=' in call.data:
        procedure = call.data.split('=')[1]
        print(procedure)
        clients[call.message.from_user.id].choosen_procedure = db.procedure_id(procedure)   #косяк с айдишником клиента
        print(clients[call.message.from_user.id].choosen_procedure)
        bf.create_dates_keyboard(bot, call.message)
    elif call.data == 'choose_procedure':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Такс, выбрайте процедуру, на которую хотите прийти', reply_markup=kb.procedures_keyboard)

    
# Запуск бота    
bot.polling(none_stop = True, interval = 0)