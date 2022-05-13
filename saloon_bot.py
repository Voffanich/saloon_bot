import telebot
from telebot import types
from credentials import apikey
from db_handler import DB_handler
import bot_funcs as bf

bot = telebot.TeleBot(apikey)

db = DB_handler()

# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(m, res=False):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что может бот?")
    btn2 = types.KeyboardButton("Записаться")
    btn3 = types.KeyboardButton("Перенести визит")
    btn4 = types.KeyboardButton("Проверить запись")
    btn5 = types.KeyboardButton("Настроить напоминания")
    btn6 = types.KeyboardButton("Прайс")
    btn7 = types.KeyboardButton("Обо мне")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(m.chat.id, text="Дорова! Здесь ты можешь записаться ко мне на процедуры. Жамкай нужные кнопки", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == 'Что может бот?'):
        bot.send_message(message.chat.id, text='1. Записаться на процедуру\n2. Посмотреть дату и время записи\n3. Настроить напоминания о визите\n4. Перенести визит\n')
    
    
    elif (message.text == 'Записаться'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        client = message.from_user.username
                
        if db.client_exists(client):
            bot.send_message(message.chat.id, text='Такс, смотри на свободные окошки', reply_markup=markup)
        else:
            btn1 = types.KeyboardButton("Оставляем")
            btn2 = types.KeyboardButton("Изменить")
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text='Впервые здесь? Давайте-ка занесем вас в базу клиентов. '
                                                    f'В телеграме вы подписаны как <b>{message.from_user.first_name} {message.from_user.last_name}</b>. '
                                                    'Оставляем или хотите изменить? Желательно записаться по реальному имени'
                                                    'и фамилии. Фамилию можно просто одной буквой с точкой написать (например Юлия М.)', reply_markup=markup, parse_mode="HTML")
            
        
    elif (message.text == 'Перенести визит'):
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
        bot.send_message(message.chat.id, text='Хорошо, оставляем. Теперь введите, пожалуйста, ваш номер телефона в формате +375хх')
                
        
    elif ('375' in message.text and 11 < len(message.text) < 14):
        phone_number = message.text
        bot.send_message(message.chat.id, text=f'Записываем ваш номер телефона {phone_number}')   
        
        db.add_client(message.from_user.username, message.from_user.first_name, message.from_user.last_name, phone_number,)
    elif (message.text == 'Изменить'):
        bot.send_message(message.chat.id, text='Ну, давайте менять')
    else:
        bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Если что-то не получается, пользуйтесь, пожалуйста, кнопками меню бота')


# Запуск бота    
bot.polling(none_stop = True, interval = 0)