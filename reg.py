import re

while True:
    m = input("Введите слово: ")
    if re.fullmatch(r'\b[а-яА-Я]{2,10}\b[ ]\b[а-яА-Я]{2,12}\b', m):
        print('Соответствует')
    else:
        print('Не соответствует')