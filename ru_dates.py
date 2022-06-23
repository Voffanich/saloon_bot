from datetime import datetime as dt
from datetime import timedelta

ru_week_days_short = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
ru_week_days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'сб', 'вс']

ru_months = [None, 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
ru_of_months = [None, 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def ru_d_short(date) -> str:
    ru_day = ru_week_days_short[int(dt.strftime(date, '%w'))]
    return ru_day

def ru_d_full(date) -> str:
    ru_day = ru_week_days[int(dt.strftime(date, '%w'))]
    return ru_day

def ru_m_full(date) -> str:
    ru_month = ru_months[int(dt.strftime(date, '%-m'))]
    return ru_month

def ru_of_m_full(date) -> str:
    ru_month = ru_of_months[int(dt.strftime(date, '%-m'))]
    return ru_month
