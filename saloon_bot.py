import telebot
from telebot import types
from credentials import apikey

bot = telebot.TeleBot(apikey)

# Обработка команды Start
@bot.message_handler(commands=['start'])
def start(m, res=False):    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Что может бот?")
    btn2 = types.KeyboardButton("Записаться")
    btn3 = types.KeyboardButton("Перенести визит")
    btn4 = types.KeyboardButton("Проверить запись")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(m.chat.id, text="Дорова! Здесь ты можешь записаться ко мне на процедуры. Жамкай нужные кнопки", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == 'Что может бот?'):
        bot.send_message(message.chat.id, text='1. Записаться на процедуру\n2. Посмотреть дату и время записи\n3. Настроить напоминания о визите\n4. Перенести визит\n')
    elif (message.text == 'Записаться'):
        bot.send_message(message.chat.id, text='Такс, смотри на свободные окошки')
    else:
        bot.send_message(message.chat.id, text='К такому меня жизнь не готовила) Напиши что-нибудь адекватное')

# Запуск бота    
bot.polling(none_stop = True, interval = 0)