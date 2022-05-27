class Client():
    
    def __init__(self, id: int, username: str = '', first_name: str = '', last_name: str = '', timing: str = '2:30', phone_number: str = ''):
        self.id = id
        self.flag = ''
        self.phone_number = phone_number
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.timing = timing
        self.admin = False
        self.chosen_procedure: str = ''
        self.dates: dict = {
        'Пн, 25 мая': ['10:00', '12:00', '18:00'],
        'Вт, 26 мая': ['12:00', '16:00'],
        'Ср, 27 мая': ['10:00', '12:00', '14:00', '16:00'],
        'Чт, 28 мая': ['10:00', '12:00', '14:00', '16:00', '18:00'],
        'Пт, 29 мая': ['10:00', '16:00'],
        'Сб, 30 мая': ['10:00', '12:00', '14:00', '16:00'],
        'Вс, 31 мая': ['10:00'],
        'Пн, 1 июня': ['10:00', '12:00', '16:00'],
        'Вт, 2 июня': ['10:00', '12:00', '14:00', '16:00'],
        'Ср, 3 июня': ['14:00', '16:00'],
        'Чт, 4 июня': ['10:00', '14:00', '16:00']        
        }