import telebot
import requests
from telebot import types

bot = telebot.TeleBot('7734365936:AAEbWFKnjERHAWcfnONG4S0J_cC1bn0mhVg')


@bot.message_handler(commands=['start'])
def main(message):
    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')

    # Затем вызываем функцию, которая отправляет меню
    menu(message)


def get_photo_of_the_day(message):
    url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'  # Используйте ваш API_KEY
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        image_url = data['url']
        explanation = data['explanation']

        # Отправляем фотографию и её описание
        bot.send_photo(message.chat.id, image_url, caption=explanation)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о фотографии дня.")


def menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Космическое фото дня', callback_data='get_photo'))
    bot.send_message(message.chat.id, 'Меню', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'get_photo')
def handle_query(call):
    get_photo_of_the_day(call.message)


bot.polling(none_stop=True)
