from datetime import date
from datetime import datetime as dt

import bot_funcs as bf
import g_funcs as gf
import ru_dates as rd
from db_handler import db

# db = DB_handler()

# RECREATE DB
# db.setup()
# db.update_procedures()

# procedures = db.get_procedures_data()
days_off = [4, 7, 12, 13, 14, 15, 21, 22, 25, 27, 28]
work_day_start = '10:00'
work_day_finish = '21:00'
window_colors = {
            "window": 10,
            "occupied_window": 6,
            "procedure": 3
        }

gf.clndr.place_windows(gf.calendar_id_2, '01:50', mode='month', days_off=days_off, work_day_start=work_day_start, work_day_finish=work_day_finish,
                       period_start='2024-04-01', period_finish='2024-04-30', window_colors=window_colors, events_gap=30, events_shift=30)

# gf.clndr.get_available_times(gf.calendar_id_2, 30, 30)



# print(rd.date_from_ru_weekday_comma_date('Вт, 5 июня'))

# print(bf.get_available_times(1))
# print(bf.get_available_times_2(procedures, 2))
# timetable = bf.get_available_times(procedures, 1, 20)

# print(timetable)

# for key in timetable:
#     print(key, timetable[key])



# print(db.get_occupied_periods(20))
# db.clear_old_db_backups(10, 'backups')



# print(db.get_procedures_data())

# procedures = db.get_procedures_data()

# db.show_visits()

# print(db.get_clients_data())

# clients = bf.create_client_objects()

# print(clients['285462822'].client_id)




# db.add_client("234637822", "voffanich", "Владимир", "Матюшев", "+375295684598")
# db.add_client("668798638", "Kalesi", "Алеся", "Матюшева", "+375295684598")
# db.add_client("239547822", "Bulba21", "Яна", "Матюшева", "+375295684598")
# db.add_client("935537822", "technozhrets", "Андрей", "Наличаев", "+375295684598")
# db.add_client("234895699", "Dmitry_1010", "Дмитрий", "Митрахович", "+375295684598")
# db.add_client("285462822", "AliaxM", "Алексей", "Мальцев", "+375295684598")

