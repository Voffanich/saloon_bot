from db_handler import DB_handler

db = DB_handler()
db.setup()


"""db.add_client("voffanich", "Владимир", "Матюшев", "+375295684598")
db.add_client("Kalesi", "Алеся", "Матюшева", "+375295684598")
db.add_client("Bulba21", "Яна", "Матюшева", "+375295684598")
db.add_client("technozhrets", "Андрей", "Наличаев", "+375295684598")
db.add_client("Dmitry_1010", "Дмитрий", "Митрахович", "+375295684598")
db.add_client("AliaxM", "Алексей", "Мальцев", "+375295684598")
"""

client_objects = []

# список клиентов из базы
clients_list = db.clients_list()

# генерация списка объектов клиентов
for client in clients_list:
    client_objects.append(client)
    
print(client_objects)