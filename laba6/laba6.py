import os  # импорт библиотеки для работы с системой
from dotenv import load_dotenv  # импорт метода для работы с переменными окружения
import telebot  # импорт библиотеки для работы с tg ботом
import requests  # импорт библиотеки для работы с запросами
from bs4 import BeautifulSoup  # импорт библиотеки для парсинга сайтов

# загрузка переменных окружения
load_dotenv()
# получения токена из переменных окружения
TOKEN = os.getenv('TOKEN')

# создания объекта класса Bot
bot = telebot.TeleBot(token=TOKEN)
# url сайта с курсом валют
url = 'https://www.banki.ru/products/currency/cb/'
# кортеж валют быстрого доступа
currencies = ('USD', 'EUR', 'AUD', 'THB', 'BYN', 'JPY')


def get_currency(currency):
    """
    Функция получения курса валют

    Args:
        currency (string): [строчное представление валюты]
    Returns:
        float: [курс переданной валюты]
    """

    # ответ на запрос получения страницы
    response = requests.get(url)
    # объект для парсинга
    bs = BeautifulSoup(response.text, 'lxml')
    # блок, содержащий необходимые данные о валюте
    tmp = bs.find('tr', attrs={'data-currency-code': currency})
    # получение курса валюты
    return f'{tmp.find_all("td")[2].text.strip()} - {float(tmp.find_all("td")[3].text.strip()):.2f}р'


def own_currency(message):
    """
    Функция получения курса валют при вводе с клавиатуры

    Args:
        message (message object): [пришедшее сообщение от пользователя]
    Returns:
        float: [курс переданной валюты]
    """

    # id пользователя
    id = message.from_user.id
    # обработка исключения, связанного с отсутствием переданной валюты на сайте
    try:
        # отправка сообщения пользователю с курсом
        bot.send_message(
            chat_id=id,
            text=get_currency(message.text)
        )
    except:
        # отправка сообщения пользователю об ошибке
        bot.send_message(
            chat_id=id,
            text='Мы не смогли найти такую валюту'
        )


# декоратор для обработки команды start
@bot.message_handler(commands=['start'])
def start(message):
    """
    Функция обработки команды start

    Args:
        message (message object): [пришедшее сообщение от пользователя]
    """

    # создания объекта для работы с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    # добавление кнопок 'Узнать курс' и 'Указать свою валюту'
    keyboard.add('Узнать курс', 'Указать свою валюту')
    # отправка сообщения пользователю
    bot.send_message(
        text='Я помогу вам узнать курс валют',
        chat_id=message.from_user.id,
        reply_markup=keyboard
    )


# декоратор для обработки текстовых сообщений
@bot.message_handler(content_types='text')
def command(message):
    """
    Функция обработки текстовых сообщений

    Args:
        message (message object): [пришедшее сообщение от пользователя]
    """

    # id пользователя
    id = message.from_user.id
    # создания объекта для кнопок создаваемых под сообщением
    markup = telebot.types.InlineKeyboardMarkup()
    # остановка всех последовательных обработчиков сообщений
    bot.clear_step_handler_by_chat_id(chat_id=id)

    # обработка кнопки 'Узнать курс'
    if message.text == 'Узнать курс':
        for currency in currencies:
            # добавление кнопок под сообщение из кортежа currencies
            markup.add(
                telebot.types.InlineKeyboardButton(
                    text=currency,
                    callback_data=currency
                )
            )
        # добавление кнопки закрытия сообщения
        markup.add(telebot.types.InlineKeyboardButton(
            text='Закрыть',
            callback_data='close'
        ))
        # отправка сообщения пользователю
        bot.send_message(
            chat_id=id,
            text='Выберите одну из валют',
            reply_markup=markup
        )
    # обработка кнопки 'Указать свою валюту'
    elif message.text == 'Указать свою валюту':
        # добавление кнопки закрытия сообщения
        markup.add(telebot.types.InlineKeyboardButton(
            text='Закрыть',
            callback_data='close'
        ))
        # отправка сообщения пользователю
        bot.send_message(
            chat_id=id,
            text='Введите свою валюту в стандартном формате',
            reply_markup=markup
        )
        # добавление последовательного обработчика сообщения
        bot.register_next_step_handler(message, own_currency)


# декоратор для обработки callback ответов
@bot.callback_query_handler(func=lambda _: True)
def currency(call):
    """
    Функция обработки callback ответов

    Args:
        call (call object): [пришедший ответ кнопок под сообщением]
    """

    # id пользователя
    id = call.message.chat.id
    # обработка callback из кортежа currencies
    if call.data in currencies:
        # отправка сообщения пользователю
        bot.send_message(
            chat_id=id,
            text=get_currency(call.data)
        )
    # обработка callback close
    elif call.data == 'close':
        # остановка всех последовательных обработчиков сообщений
        bot.clear_step_handler_by_chat_id(chat_id=id)
        # удаление сообщения откуда пришел callback
        bot.delete_message(
            chat_id=id,
            message_id=call.message.message_id
        )


# обработка случая вызова файла напрямую
if __name__ == '__main__':
    # создание отдельных потоков для разных пользователей
    bot.polling()
