#help - все команды +
#weather - погода +
#viki - википедия +
#random - рандомное число +
import config
import telebot
import random
from telebot import types
import requests
import pyowm
import wikipedia

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, крутой бот от Антохи в Telegram.\nЧтобы узнать мои команды введите /help".format(message.from_user, bot.get_me()),
		parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, "/help - все команды\n/weather - погода\n/viki <слово или фраза кторое хотите найти> - википедия (пример: /viki птицы)\n/random <начальное число> <конечное число> - рандомное число (пример: /random 1 100)")

@bot.message_handler(commands=['random'])
def randomm(message):
	if message.text == '/random':
		bot.send_message(message.chat.id, "Введике как в примере. Если не знаете как напишите /help")
		exit(0)
	a = message.text
	a = a[7:]
	first = a
	second = ''
	for i in range(len(a)):
		if a[i] == ' ':
			first = a[i+1:]
		else:
			break
	a = ''
	for i in range(len(first)):
		if first[i] == ' ':
			second = first[i+1:]
			first = first[:i]
			break
	for i in range(len(second)):
		if second[i] == ' ':
			a = second[i:]
			break
	if first[len(first)-1] == ' ' or second[0] == ' ' or a != '':
		bot.send_message(message.chat.id, "Введике как в примере. Если не знаете как напишите /help")
		exit(0)
	bot.send_message(message.chat.id, random.randint(int(first),int(second)))

@bot.message_handler(commands=['weather'])
def weather(message):
	markup = types.InlineKeyboardMarkup(row_width=2)
	item1 = types.InlineKeyboardButton("Осиповичи", callback_data='Asipovichy')
	item2 = types.InlineKeyboardButton("Минск", callback_data='Minsk')
	markup.add(item1, item2)
	bot.send_message(message.chat.id, "Выберете город:", reply_markup=markup)

l = []
o = []
@bot.message_handler(commands=['viki'])
def viki(message):
	a = message.text
	if a == '/viki':
		bot.send_message(message.chat.id, "Введике как в примере. Если не знаете как напишите /help")
		exit(0)
	for i in range(len(a)):
		if a[i] == ' ':
			first = a[i+1:]
	wikipedia.set_lang("ru")
	p = wikipedia.search(first)
	if p != []:
		for i in range(len(p)):
			o.append(p[i])
		markup = types.InlineKeyboardMarkup(row_width=len(p))
		for i in range(len(p)):
			l.append(types.InlineKeyboardButton(p[i], callback_data='ZHdfhsr12v' + str(i)))
		for i in range(len(l)):
			markup.add(l[i])
		bot.send_message(message.chat.id, "Вот что мне удалось найти:", reply_markup=markup)
	else:
		bot.send_message(message.chat.id, "Мне ничего не удалось найти")

@bot.message_handler(content_types=['text'])
def main(message):
	bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'Asipovichy' or 'Minsk':
				owm = pyowm.OWM('d2eedfc4b72765594709200c9b411d83')
				observation = owm.weather_at_place(str(call.data))
				w = observation.get_weather()
				a = w.get_temperature('celsius')['temp']
				f = w.get_humidity()
				if call.data == 'Asipovichy':
					bot.send_message(call.message.chat.id, "В Осиповичах\n" + "Текущая температура: " + str(round(a)) + 
						" °C" + "\n" + "Влажность: " + str(f) + " %", reply_markup=None)
				elif call.data == 'Minsk':
					bot.send_message(call.message.chat.id, "В Минске\n" + "Текущая температура: " + str(round(a)) + 
						" °C" + "\n" + "Влажность: " + str(f) + " %", reply_markup=None)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберете город:",
						reply_markup=None)
				exit(0)
		if call.message:
			for i in range(len(l)):
				if call.data == 'ZHdfhsr12v' + str(i):
					bot.send_message(call.message.chat.id, wikipedia.summary(o[i]))
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот что мне удалось найти:",
						reply_markup=None)
					l.clear()
					o.clear()
					break
	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)