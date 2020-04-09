#help - все команды +
#weather - погода +
#viki - википедия
#random - рандомное число +
import config
import telebot
import random
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, крутой бот от Антохи в Telegram.\nЧтобы узнать мои команды введите /help".format(message.from_user, bot.get_me()),
		parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "/help - все команды\n/weather - погода\n/random - рандомное число(от 0 до 100)")

@bot.message_handler(commands=['random'])
def randomm(message):
	if message.text == '/random':
		bot.send_message(message.chat.id, "Введике как в примере. Если не знаете как напишите /help")
		exit(0)
	a = message.text
	first = ''
	second = ''
	for i in range(len(a)):
		if a[i] == ' ':
			first = a[i+1:]
			break
	for i in range(len(first)):
		if first[i] == ' ':
			second = int(first[i+1:])
			first = int(first[:i])
			break
	bot.send_message(message.chat.id, random.randint(first,second))

@bot.message_handler(commands=['weather'])
def weather(message):
	owm = pyowm.OWM('d2eedfc4b72765594709200c9b411d83')
	observation = owm.weather_at_place('Asipovichy')
	w = observation.get_weather()
	a = w.get_temperature('celsius')['temp']
	f = w.get_humidity()
	bot.send_message(message.chat.id, "Текущая температура: " + str(round(a)) + " °C" + "\n" + "Влажность: " + str(f) + " %")

#@bot.message_handler(commands=['viki'])
#def viki(message):
#	bot.send_message(message.chat.id, "Эта команда пока что не работает")

@bot.message_handler(content_types=['text'])
def main(message):
	bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


bot.polling(none_stop=True)