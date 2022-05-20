class Client():
    
    def __init__(self, id: int = '0', username: str = '', first_name: str = '', last_name: str = '', timing: str = '2:30',phone_number: str = ''):
        self.id = id
        self.flag = ''
        self.phone_number = phone_number
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.timing = timing
        self.admin = False
        