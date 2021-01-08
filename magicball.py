import random
from time import sleep

class Ball():
    ANSWERS = {
            'positive': ['Невозможное Да!', 'Да-да-да!', 'Не мешкай! Да', 'Будь уверен(а)!'],
            'possible': ['Думаю, что да.', "Можеть быть.", "Есть перспективы", 'Звезды говорят - "Да".'],
            'neutral': ["Тут я не помощник.", "Спроси еще разок.", "Воздержусь.", "Это не ко мне."],
            'negative': ['No! Ні! Nein! Нет!', "Мой ответ - 'Нет'", "Все запутанно. Остановимся на 'НЕТ!'"],
            }

    def choose(self):
        choices = list(self.ANSWERS.keys())
        destiny = random.choice(choices)
        answer = random.choice(self.ANSWERS.get(destiny))
        return answer
