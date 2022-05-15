import telebot
from telebot import types
from credentials import apikey
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


# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(message, res=False):    
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
    if ('375' in message.text and 11 < len(message.text) < 14):
        phone_number = message.text
        
        if phone_number[0] != "+" and len(phone_number) == 12:
            phone_number = "+" + phone_number
        
        for symbol in phone_number:
            if symbol != '+' and symbol not in "0123456789":
                bot.send_message(message.chat.id, text='Вы ввели некорректный номер телефона. Введите, пожалуйста, правильный в формате +375хх')
           
        client.phone_number = phone_number    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Телефон верный")
        btn2 = types.KeyboardButton("Изменить номер телефона")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Номер телефона <b>{client.phone_number}</b> верный?', parse_mode='HTML', reply_markup=markup)
        client.flag = '' 
    else:
        bot.send_message(message.chat.id, text='Вы ввели некорректный номер телефона. Введите, пожалуйста, правильный в формате +375хх')

@bot.message_handler(func=lambda _: client.flag == 'проверить имя')
def verify_name(message):
    if re.fullmatch(r'\b[а-яА-Я]{2,10}\b[ ]\b[а-яА-Я]{2,12}\b', message.text):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        name = string.capwords(message.text)
        btn1 = types.KeyboardButton("Да, имя верное")
        btn2 = types.KeyboardButton("Изменить имя")
        client.flag = ''
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=f'Записываем вас под именем {name}?', reply_markup=markup)
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
            bot.send_message(message.chat.id, text='Такс, смотри на свободные окошки', reply_markup=markup)
        else:
            btn1 = types.KeyboardButton("Оставляем")
            btn2 = types.KeyboardButton("Изменить имя")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text='Впервые здесь? Давайте-ка занесем вас в базу клиентов. '
                                                    f'В телеграме вы подписаны как <b>{client.first_name} {client.last_name}</b>. '
                                                    'Оставляем или хотите изменить? Желательно записаться по реальному имени '
                                                    'и фамилии. Фамилию можно просто одной буквой с точкой написать (например Юлия М.)', reply_markup=markup, parse_mode="HTML")
                    
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
        bot.send_message(message.chat.id, text='Хорошо. Теперь введите ваш номер телефона в формате +375хх')
        client.flag = 'проверить телефон'        
        
        
    elif (message.text == 'Изменить имя'):
        bot.send_message(message.chat.id, text='Введите, пожалуйста, ваши имя и фамилию в формате <b>Имя Фамилия</b>', parse_mode='HTML')
        client.flag = 'проверить имя' 
    
    
    elif (message.text == 'Изменить номер телефона'):
        bot.send_message(message.chat.id, text='введите ваш номер телефона в формате +375хх')
        client.flag = 'проверить телефон' 
    
    
    elif (message.text == 'Да, имя верное'):
        bot.send_message(message.chat.id, text='Чудненько! Теперь введите ваш номер телефона в формате +375хх')
        client.flag = 'проверить телефон'
    
    
    elif (message.text == 'Телефон верный'):
        bot.send_message(message.chat.id, text=f'Чудненько, сохранили вас в базе клиентов как {client.first_name} {client.last_name}, {client.phone_number}')
        db.add_client(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, client.phone_number)        
        client.flag = 'выбор процедуры'
                    
        
    else:
        bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота')


    
# Запуск бота    
bot.polling(none_stop = True, interval = 0)