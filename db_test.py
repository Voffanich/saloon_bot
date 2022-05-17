from db_handler import DB_handler
import bot_funcs as bf

db = DB_handler()
db.setup()


#db.add_client("234637822", "voffanich", "Владимир", "Матюшев", "+375295684598")
"""db.add_client("234637232", "Kalesi", "Алеся", "Матюшева", "+375295684598")
db.add_client("239547822", "Bulba21", "Яна", "Матюшева", "+375295684598")
db.add_client("935537822", "technozhrets", "Андрей", "Наличаев", "+375295684598")
db.add_client("234895699", "Dmitry_1010", "Дмитрий", "Митрахович", "+375295684598")
db.add_client("285462822", "AliaxM", "Алексей", "Мальцев", "+375295684598")"""


"""
client_objects = []

# список клиентов из базы
clients_list = db.clients_list()

# генерация списка объектов клиентов
for client in clients_list:
    client_objects.append(client)
    
print(client_objects)
"""

print(bf.get_procedures())