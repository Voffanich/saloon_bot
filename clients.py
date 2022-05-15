from unicodedata import name


class Clients():
    
    def __init__(self, id: str = '', username: str = '', first_name: str = '', last_name: str = '', timing: str = '2:30',phone_number: str = ''):
        self.client_id = id
        self.flag = ''
        self.phone_number = phone_number
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.timing = timing
        