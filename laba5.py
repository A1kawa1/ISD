import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(token='5999197476:AAEht2HSt2sqGCmCwlLuGKU3hn2JAJrKLSg')
url = 'https://www.banki.ru/products/currency/cb/'
currencies = ('USD', 'EUR', 'AUD', 'THB', 'BYN', 'JPY')


def get_currency(currency):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'lxml')
    tmp = bs.find('tr', attrs={'data-currency-code': currency})
    return f'{tmp.find_all("td")[2].text.strip()} - {float(tmp.find_all("td")[3].text.strip()):.2f}р'


def own_currency(message):
    id = message.from_user.id
    try:
        bot.send_message(
            chat_id=id,
            text=get_currency(message.text)
        )
    except:
        bot.send_message(
            chat_id=id,
            text='Мы не смогли найти такую валюту'
        )


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.add('Узнать курс', 'Указать свою валюту')
    bot.send_message(
        text='Я помогу вам узнать курс валют',
        chat_id=message.from_user.id,
        reply_markup=keyboard
    )


@bot.message_handler(content_types='text')
def command(message):
    id = message.from_user.id
    markup = telebot.types.InlineKeyboardMarkup()
    bot.clear_step_handler_by_chat_id(chat_id=id)

    if message.text == 'Узнать курс':
        for currency in currencies:
            markup.add(
                telebot.types.InlineKeyboardButton(
                    text=currency,
                    callback_data=currency
                )
            )
        markup.add(telebot.types.InlineKeyboardButton(
            text='Закрыть',
            callback_data='close'
        ))
        bot.send_message(
            chat_id=id,
            text='Выберите одну из валют',
            reply_markup=markup
        )
    elif message.text == 'Указать свою валюту':
        markup.add(telebot.types.InlineKeyboardButton(
            text='Закрыть',
            callback_data='close'
        ))
        bot.send_message(
            chat_id=id,
            text='Введите свою валюту в стандартном формате',
            reply_markup=markup
        )
        bot.register_next_step_handler(message, own_currency)


@bot.callback_query_handler(func=lambda _: True)
def currency(call):
    id = call.message.chat.id
    if call.data in currencies:
        bot.send_message(
            chat_id=id,
            text=get_currency(call.data)
        )
    elif call.data == 'close':
        bot.clear_step_handler_by_chat_id(chat_id=id)
        bot.delete_message(
            chat_id=id,
            message_id=call.message.message_id
        )


if __name__ == '__main__':
    bot.polling()
