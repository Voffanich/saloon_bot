from datetime import datetime as dt
from datetime import timedelta
from datetime import date

ru_week_days_short = [ 'вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'] # %w - number of weekday, 0 - Sunday
ru_week_days = ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'] # %w - number of weekday, 0 - Sunday

ru_months = [None, 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
ru_of_months = [None, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def ru_d_short(date_obj) -> str:
    ru_day = ru_week_days_short[int(dt.strftime(date_obj, '%w'))]
    return ru_day

def ru_d_full(date_obj) -> str:
    ru_day = ru_week_days[int(dt.strftime(date_obj, '%w'))]
    return ru_day

def ru_m_full(date_obj) -> str:
    ru_month = ru_months[int(dt.strftime(date_obj, '%m'))]
    return ru_month

def ru_of_m_full(date_obj) -> str:
    ru_month = ru_of_months[int(dt.strftime(date_obj, '%m'))]
    return ru_month

# returns date_obj as for exapmle 'Пн, 5 июля'
def ru_weekday_comma_date(date_obj) -> str:
    ru_date = ru_d_short(date_obj).capitalize() + ', ' + dt.strftime(date_obj, '%d') + ' ' + ru_of_m_full(date_obj)
    return ru_date

# reverse function for the previous one. Returns date_obj object from string like 'Пн, 5 июля'
def date_from_ru_weekday_comma_date(date_str: str):
    year = date.today().year
    for i in range(1, len(ru_of_months)):
        if ru_of_months[i] == date_str.split(' ')[-1]:
            month = i
    date_obj = dt.strptime(f'{year}{date_str.split(" ")[-2]} {str(month)}', '%Y%d %m')
    if date_obj < dt.now():
        year += 1
        date_obj = dt.strptime(f'{year}{date_str.split(" ")[-2]} {str(month)}', '%Y%d %m')
    
    return date_obj