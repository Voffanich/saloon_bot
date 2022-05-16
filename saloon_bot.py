import telebot
from telebot import types
from credentials import apikey, admin_usernames
from db_handler import DB_handler
import bot_funcs as bf
from clients import Clients
import re
import string

bot = telebot.TeleBot(apikey)

client_objects = []
db = DB_handler()
client = Clients()

"""# список клиентов из базы
clients_list = db.clients_list()

# генерация списка объектов клиентов
for client in clients_list:
    client_objects.append(Clients(client))"""

# клавиатура выбора процедур
procedures_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
procedures = ['Маникюр', 'Педикюр', 'Ламинирование ресниц']
for procedure in procedures:
    procedures_keyboard.add(types.KeyboardButton(procedure))

# клавиатура админа
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)   
btn1 = types.KeyboardButton("Посмотреть записи")
btn2 = types.KeyboardButton("Обновить прайс")
btn3 = types.KeyboardButton("Скачать шаблон прайса")
btn4 = types.KeyboardButton("Обновить процедуры")
btn5 = types.KeyboardButton("Скачать шаблон процедур")
btn6 = types.KeyboardButton("Скачать файл окошек")
btn7 = types.KeyboardButton("Посмотреть свободные окна")
admin_keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(message, res=False):
    if client.admin == False:    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Что может бот?")
        btn2 = types.KeyboardButton("Записаться")
        btn3 = types.KeyboardButton("Перенести/отменить визит")
        btn4 = types.KeyboardButton("Проверить запись")
        btn5 = types.KeyboardButton("Настроить напоминания")
        btn6 = types.KeyboardButton("Прайс")
        btn7 = types.KeyboardButton("Обо мне")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        bot.send_message(message.chat.id, text="Дорова! Здесь ты можешь записаться ко мне на процедуры. Жамкай нужные кнопки", reply_markup=markup)
           
@bot.message_handler(func=lambda _: client.flag == 'проверить телефон')
def verify_phone_number(message):
    phone_number = message.text
    if re.fullmatch(r'[+]?375(29|33|44|25)\d{7}\b', phone_number):
        
        if phone_number[0] != "+" and len(phone_number) == 12:
            phone_number = "+" + phone_number
       
        client.phone_number = phone_number    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Телефон верный")
        btn2 = types.KeyboardButton("Изменить номер телефона")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Номер телефона <b>{client.phone_number}</b> верный?', parse_mode='HTML', reply_markup=markup)
        client.flag = '' 
    else:
        bot.send_message(message.chat.id, text='Вы ввели некорректный номер телефона. Введите, пожалуйста, правильный в формате +375хх без пробелов и дефисов')

@bot.message_handler(func=lambda _: client.flag == 'проверить имя')
def verify_name(message):
    if re.fullmatch(r'\b[а-яА-Я]{2,10}\b[ ]\b[а-яА-Я]{2,12}\b', message.text):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        name = string.capwords(message.text).split(' ')
        client.first_name = name[0]
        client.last_name = name[1]
        btn1 = types.KeyboardButton("Да, имя верное")
        btn2 = types.KeyboardButton("Изменить имя")
        client.flag = ''
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Записываем вас под именем <b>{client.first_name} {client.last_name}</b>?', reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, text=f'Вы ввели некорректное имя. Введите, пожалуйста, имя и фамилия в формате <b>Имя Фамилия</b>', parse_mode="HTML")
        client.flag = 'проверить имя'
    
@bot.message_handler(content_types=['text'])
def func(message):
    
    
    if (message.text == 'Что может бот?'):
        bot.send_message(message.chat.id, text='1. Записаться на процедуру\n2. Посмотреть дату и время записи\n3. Настроить напоминания о визите\n4. Перенести визит\n')
            
    
    elif (message.text == 'Записаться'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        client.username = message.from_user.username
        client.first_name = message.from_user.first_name
        client.last_name = message.from_user.last_name
                
        if db.client_exists(client.username):
            bot.send_message(message.chat.id, text='Такс, выбрайте процедуру, на которую хотите прийти', reply_markup=procedures_keyboard)
        else:
            btn1 = types.KeyboardButton("Оставляем")
            btn2 = types.KeyboardButton("Изменить имя")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text='Впервые здесь? Давайте-ка занесем вас в базу клиентов. '
                                                    f'В телеграме вы подписаны как <b>{client.first_name} {client.last_name}</b>. '
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
        client.flag = 'проверить телефон'        
        
        
    elif (message.text == 'Изменить имя'):
        bot.send_message(message.chat.id, text='Введите, пожалуйста, ваши имя и фамилию в формате <b>Имя Фамилия</b>. Желательно записаться по реальному имени и фамилии. Фамилию можно просто одной буквой с точкой написать (например Юлия М.)', parse_mode='HTML')
        client.flag = 'проверить имя' 
    
    
    elif (message.text == 'Изменить номер телефона'):
        bot.send_message(message.chat.id, text='введите ваш номер телефона в формате +375хх без пробелов и дефисов')
        client.flag = 'проверить телефон' 
    
    
    elif (message.text == 'Да, имя верное'):
        bot.send_message(message.chat.id, text='Чудненько! Теперь введите ваш номер телефона в формате +375хх без пробелов и дефисов')
        client.flag = 'проверить телефон'
    
    
    elif (message.text == 'Телефон верный'):
        bot.send_message(message.chat.id, text=f'Чудненько, сохранили вас в базе клиентов как {client.first_name} {client.last_name}, {client.phone_number}', reply_markup='')
        db.add_client(message.from_user.id, message.from_user.username, client.first_name, client.last_name, client.phone_number)        
        client.flag = 'выбор процедуры'
        
        
    elif (message.text == 'admino' or message.text == 'админо'):                
        if message.from_user.username in admin_usernames:
            bot.send_message(message.chat.id, text='Привет, админ!', reply_markup=admin_keyboard)
            client.admin = True
        else:
            bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота', reply_markup=markup_main_menu)
           
        
    else:
        bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота')


    
# Запуск бота    
bot.polling(none_stop = True, interval = 0)