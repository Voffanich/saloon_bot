from datetime import date
from datetime import datetime as dt

import bot_funcs as bf
import ru_dates as rd
from db_handler import db

# db = DB_handler()

# RECREATE DB
# db.setup()
# db.update_procedures()

procedures = db.get_procedures_data()



# print(rd.date_from_ru_weekday_comma_date('Вт, 5 июня'))

# print(bf.get_available_times(1))
# print(bf.get_available_times_2(procedures, 2))
timetable = bf.get_available_times(procedures, 1, 20)

for key in timetable:
    print(key, timetable[key])


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

