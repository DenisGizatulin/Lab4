import telebot
import requests

import datetime
from googletrans import Translator

from telebot import types

class SpaceBot:
    def __init__(self, api_token):
        self.bot = telebot.TeleBot(api_token)
        self.translator = Translator()
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def main(message):
            self.bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
            self.menu(message)

        @self.bot.callback_query_handler(func=lambda call: call.data in ['get_photo', 'people_in_space', 'photo_by_date'])
        def handle_query(call):
            if call.data == 'get_photo':
                self.get_photo_of_the_day(call.message)
            elif call.data == 'people_in_space':
                self.people_in_space(call.message)
            elif call.data == 'photo_by_date':
                self.bot.send_message(call.message.chat.id, "Введите дату в формате ГГГГ-ММ-ДД:")
                self.bot.register_next_step_handler(call.message, self.process_date_input)

    def menu(self, message):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Космическое фото дня', callback_data='get_photo'))
        markup.add(types.InlineKeyboardButton('Сколько людей сейчас в космосе', callback_data='people_in_space'))
        markup.add(types.InlineKeyboardButton('Дата', callback_data='photo_by_date'))
        self.bot.send_message(message.chat.id, 'Меню: ', reply_markup=markup)



    def get_photo_of_the_day(self, message):
        url = 'https://api.nasa.gov/planetary/apod?api_key=wW8ahl4j6ZoIsbV7vJ9bbvh4Gagjy3nKhoV2hqiJ'
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            image_url = data['url']
            explanation = data['explanation']
            translated_explanation = self.translator.translate(explanation, dest='ru').text

            # Проверяем длину переведенного объяснения
            if len(translated_explanation) < 1024:
                self.bot.send_photo(message.chat.id, image_url, caption=translated_explanation)
            else:
                # Отправляем картинку отдельно
                self.bot.send_photo(message.chat.id, image_url)
                # Отправляем текст отдельным сообщением
                self.bot.send_message(message.chat.id, translated_explanation)
        else:
            self.bot.send_message(message.chat.id, "Не удалось получить данные о фотографии дня.")

    def get_photo_of_the_day_by_date(self, message, date):
        # Формат даты должен быть 'YYYY-MM-DD'
        url = 'https://api.nasa.gov/planetary/apod?api_key=wW8ahl4j6ZoIsbV7vJ9bbvh4Gagjy3nKhoV2hqiJ&date=' + str(date)
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            image_url = data['url']
            explanation = data['explanation']

            # Переводим описание на русский язык
            translated_explanation = self.translator.translate(explanation, dest='ru').text

            # Отправляем фотографию и переведённое описание
            self.bot.send_photo(message.chat.id, image_url, caption=translated_explanation)
        else:
            self.bot.send_message(message.chat.id, "Не удалось получить данные о фотографии дня.")

    def process_date_input(self, message):
        date = message.text
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            self.get_photo_of_the_day_by_date(message, date)
        except ValueError:
            self.bot.send_message(message.chat.id, "Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
            self.bot.register_next_step_handler(message, self.process_date_input)

    def people_in_space(self, message):
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
            self.bot.send_message(message.chat.id, response_text)
        else:
            self.bot.send_message(message.chat.id, "Не удалось получить данные о людях в космосе.")


    def run(self):
        self.bot.polling()

# Usage
if __name__ == "__main__":
    api_token = '7734365936:AAEbWFKnjERHAWcfnONG4S0J_cC1bn0mhVg'
    space_bot = SpaceBot(api_token)
    space_bot.run()