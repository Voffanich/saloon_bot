def get_client_data():
    print('f')
    
def test_func(message, bot):
    bot.send_message(message.chat.id, text=f'СООБЩЕНИЕ ИЗ ФУНКЦИИ! В ответ на {message.text}')