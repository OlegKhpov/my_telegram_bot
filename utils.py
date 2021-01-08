import re
from random import randint, choice


def greeting():
    GREET = [
        'Приветики-пистолетики',
        'Вiтаю',
        'Здоровеньки були',
        'Bonjour',
    ]
    return choice(GREET)


def find_sub_string(string):
    return re.split("\W+", string)


def throwDice():
    d = randint(1, 6)
    return d


def find_ru_hi(string):
    for word in find_sub_string(string):
        if word.lower() == 'привет':
            return True