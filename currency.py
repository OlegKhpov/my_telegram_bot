import requests


def get_privat_bank():
    resp = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    usd = resp.json()[0]
    eur = resp.json()[1]
    return f"Курс по Привату:\
        \nДоллар 💵: {float(usd.get('buy')):.2f}\
        \nЕвро 💶: {float(eur.get('buy')):.2f}"


def skoka(money=0):
    resp = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    usd = resp.json()[0].get('buy')
    eur = resp.json()[1].get('buy')
    if money == 0:
        return f'Нужно ввести правильный запрос.'
    return f"За {money} грн получается:\
        \n{money/float(usd):.2f} $ 💵\
        \n{money/float(eur):.2f} € 💶"