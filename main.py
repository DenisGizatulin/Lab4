import telebot

bot = telebot.TeleBot('7734365936:AAEbWFKnjERHAWcfnONG4S0J_cC1bn0mhVg')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет')

bot.polling(none_stop=True)