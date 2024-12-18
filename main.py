import telebot
import requests
from telebot import types
from googletrans import Translator

bot = telebot.TeleBot('7734365936:AAEbWFKnjERHAWcfnONG4S0J_cC1bn0mhVg')
translator = Translator()  # Инициализируем переводчика


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    menu(message)


def get_photo_of_the_day(message):
    url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        image_url = data['url']
        explanation = data['explanation']

        # Переводим описание на русский язык
        translated_explanation = translator.translate(explanation, dest='ru').text

        # Отправляем фотографию и переведённое описание
        bot.send_photo(message.chat.id, image_url, caption=translated_explanation)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о фотографии дня.")


def people_in_space(message):
    url = 'http://api.open-notify.org/astros.json'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        people = data['people']

        # Формируем сообщение с информацией о людях в космосе
        response_text = "В космосе сейчас находятся следующие астронавты:\n\n"

        for i, person in enumerate(people, start=1):  # Используем enumerate для индексации
            response_text += f"{i}. {person['name']} на {'МКС' if person['craft'] == 'ISS' else 'Тяньгун'}\n"

        # Отправляем сообщение
        bot.send_message(message.chat.id, response_text)
    else:
        bot.send_message(message.chat.id, "Не удалось получить данные о людях в космосе.")


def menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Космическое фото дня', callback_data='get_photo'))
    markup.add(types.InlineKeyboardButton('Сколько людей сейчас в космосе', callback_data='people_in_space'))
    bot.send_message(message.chat.id, 'Меню: ', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['get_photo', 'people_in_space'])
def handle_query(call):
    if call.data == 'get_photo':
        get_photo_of_the_day(call.message)
    elif call.data == 'people_in_space':
        people_in_space(call.message)


if __name__ == '__main__':
    bot.polling(none_stop=True)