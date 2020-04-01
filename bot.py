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

#weather
r = requests.get('https://pogoda7.ru/prognoz/gorod140335-Belarus-Mahilyowskaya_Voblasts-Asipovichy/1days/full')
html = r.text
soup = BeautifulSoup(html, 'lxml')
t = soup.find('div', class_="current_data")
te = t.find('div', class_="grid precip").find('div', class_="temperature").text
text1 = t.find('div', class_="grid precip").find('div', class_="cloud").text
text2 = t.find('div', class_="grid precip").find('div', class_="precipitation").text
text = text1 + " " + text2

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
	bot.send_message(message.chat.id, str(random.randint(0,100)))
	#bot.send_message(message.chat.id, "Ведите начальное число") 
	#a = message.text
	#bot.send_message(message.chat.id, "Ведите конечное число") 
	#b = message.text
	#int(a)
	#int(b)
	#import random
	#bot.send_message(message.chat.id, str(random.randint(a,b)))

@bot.message_handler(commands=['weather'])
def weather(message):
	bot.send_message(message.chat.id, "Текущая температура: " + te + "\n" + text)

#@bot.message_handler(commands=['viki'])
#def viki(message):
#	bot.send_message(message.chat.id, "Эта команда пока что не работает")

@bot.message_handler(content_types=['text'])
def main(message):
	bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


bot.polling(none_stop=True)