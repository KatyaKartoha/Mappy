import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  ...")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    colours =  message.text.split()[-1]
    city_name = message.text.split()[-2]
    manager.get_coordinates(city_name)
    manager.create_grapf('img/city.png',[city_name], colours)
    bot.send_photo(message.chat.id, photo=open('img/city.png', 'rb'))


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    colours =  message.text.split()[-1]
    cities = manager.select_cities(message.chat.id)
    manager.create_grapf('img/cities.png', cities, colours)
    bot.send_photo(message.chat.id, photo=open('img/cities.png', 'rb'))


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
