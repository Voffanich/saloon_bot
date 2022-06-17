import time
from multiprocessing.context import Process
import schedule
 
def send_message1():
    bot.send_message(USERID, 'TEXT')
 
schedule.every().day.at("08:00").do(send_message1)
 
 
class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
 
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
 
 
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
    
# https://www.cyberforum.ru/python-api/thread2572468.html