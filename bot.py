import telebot
import os

from time import sleep
from flask import Flask, request
from telebot.apihelper import answer_inline_query
from telebot.types import InlineKeyboardButton
from io import BytesIO

from utils import *
from weather import *
from magicball import Ball
from currency import get_privat_bank, skoka
from f_busta import f_busta

TOKEN = 'YOUR_TOKEN_HERE'  # insert your token here
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
b = f_busta.Booksearch()

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    if message.text.lower() == "/start":
        bot.reply_to(message, f'Привет, {message.from_user.first_name}, введи ка еще /help')
    if message.text.lower() == '/help':
        bot.send_message(
        message.chat.id,
        'Команды:\
        \n/start - помощь или /help\
        \n/dice - бросить кубик\
        \n/wnow - погода в Измаиле прям щас\
        \n/ball8 - магический шар\
        \n/pb - курс по Привату\
        \n/book [слово] - найти книгу',
        )


@bot.message_handler(commands=['dice'])
def send_dice(message):
    bot.send_message(message.chat.id,'Бросаю кубик. тебе выпало: '+str(throwDice()))


@bot.message_handler(commands=['wnow'])
def send_weather(message):
    bot.reply_to(message, text=get_weather_now())

@bot.message_handler(commands=['ball8'])
def send_ball8(message):
    msg = bot.reply_to(message, 'Шар Готов!\nВведите свой вопрос!')
    bot.register_next_step_handler(msg, ball_question)


@bot.message_handler(commands=['pb'])
def send_current(message):
    bot.reply_to(message, text=get_privat_bank())


@bot.message_handler(commands=['skoka'])
def convert_skoka(message):
    msg = message.text.split(' ')
    if len(msg) != 2 or not msg[1].isnumeric():
        bot.send_message(message.chat.id, 'Чёт пошло не так повтори запрос.')
    else:
        bot.reply_to(message, text=skoka(int(msg[1])))

@bot.message_handler(commands=['book'])
def get_book(message):
    find = message.text.split(' ')
    if len(find) <= 1:
        return bot.send_message(message.chat.id, 'После /book должно быть хоть что-то!')
    find_string = ''
    for f in find[1:]:
        find_string += f + " "    
    reply = b.search(find_string)
    if reply == '' or reply == ' ':
        bot.send_message(message.chat.id, 'Упс. Ничего не найдено')
    else:
        bot.send_message(message.chat.id, reply, reply_markup=gen_markup(b.get_pages()))

@bot.message_handler(regexp=r'/\w\d+|/\w\d+.+') 
def work_with_links_book(message):
    text = message.text
    if text.startswith((
        '/b',
        '/a',
        '/s',
        '/g',
    )):
        if '@' in text:
            text = text[:text.index('@')]
        subject = text[1]
        if subject == 's':
            subject = 'sequence'
        link = text[2:]
        url = f"/{subject}/{link}"
        b = f_busta.Booksearch()
        reply = b.search(url)
        if subject == 'b':
            bot.send_message(message.chat.id, reply, reply_markup=gen_download_markup(b.get_links()))
        else:
            bot.send_message(message.chat.id, reply)


def ball_question(message):
    ball = Ball()
    try:
        bot.reply_to(message, 'Ищу ответ')
        sleep(randint(1,5))
        bot.reply_to(message, f'Ответ! - "{ball.choose()}"')
    except:
        bot.reply_to(message, 'ERROR: ХАЛЕПА')

@bot.callback_query_handler(func=lambda call: True)
def pages_change(call):
    if call.data.isnumeric():
        s = b.find_search_words_in_msg(call.message.text)
        search = b.search(s, call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=search,
            reply_markup=gen_markup(b.get_pages())
        )
    else:
        response = requests.get(b.BASE_URL + call.data, allow_redirects=True)
        file = BytesIO(response.content)
        filename_data = response.headers['Content-Disposition']
        file_name = re.findall('filename="(.+)"', filename_data)
        if not len(file_name):
            file_name = re.findall('filename=(.+)', filename_data)
        file.name = file_name[0]
        bot.send_document(
            chat_id=call.message.chat.id,
            data=file,
        )
        

def gen_markup(set):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2
    if set[0] is not None:
        markup.add(InlineKeyboardButton(
            text=f'< {str(int(set[0]) + 1)}',
            callback_data=set[0],
        ))
    if set[1] is not None:
        markup.add(InlineKeyboardButton(
            text=f'> {str(int(set[1]) + 1)}',
            callback_data=set[1]
        ))
    return markup


def gen_download_markup(list_of_links):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 4
    for name, link in list_of_links:
        markup.add(InlineKeyboardButton(
            text=name,
            callback_data=link,
        ))
    return markup

#@bot.message_handler(content_types = ['sticker'])
#def gotStickerId(message):
#    print(message)

@bot.message_handler(content_types = ['text'])
def send_text(message):
    if find_ru_hi(message.text.lower()):
        bot.send_message(message.chat.id, f'{greeting()}, {message.from_user.first_name}!')
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Нет, не уходи!')


# Webhooks section
@server.route('/'+TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='HEROKU_CLI_URL'+TOKEN)  # this bot for heroku to make it with webhooks get CLI url
    return "!", 200


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))