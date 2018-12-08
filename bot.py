
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import config
import dbworker as bd
import apiai, json
import requests_classes as rc
from stop_words import get_stop_words
import textdistance
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from gensim.models import KeyedVectors

from geopy.distance import great_circle
import pandas as pd



	
epsilon = 0.001
bot = telebot.TeleBot(config.token)

path = 'all.norm-sz100-w10-cb0-it1-min100.w2v'
model = KeyedVectors.load_word2vec_format(path, binary=True, unicode_errors='ignore')
model.init_sims(replace=True)


def near_request(text):
	# Remove stopwords.
	stop_words = get_stop_words('russian')
	text = [w for w in text.lower().split() if w not in stop_words]
	dist1 = 0
	for s in rc.class1:
		s = [w for w in s.lower().split() if w not in stop_words]
		dist1 += model.wmdistance(s, text)
	dist2 = 0
	for s in rc.class2:
		s = [w for w in s.lower().split() if w not in stop_words]
		dist2 += model.wmdistance(s, text)

	if abs(dist1 - dist2) < epsilon or dist1 == float('inf') or dist2 == float('inf'):
		return 3
	else:
		if dist1 < dist2:
			return 1 # sights
		else:
			return 2 # notifications

def define_station(text):
	stop_words = get_stop_words('russian')
	text = ' '.join([w for w in text.lower().split() if w not in stop_words])
	min_dist = float('inf')
	word = ''
	for s in rc.class3:
	    s = ' '.join([w for w in s.lower().split() if w not in stop_words])

	    dist3 = textdistance.hamming(s, text)
	    if dist3 < min_dist:
	        
	        min_dist = dist3
	        word = s
	return word

def changes(text):
	stop_words = get_stop_words('russian')
	s = ''
	text_lst = []
	for w in text.lower().split():
	    if w not in stop_words:
	        s += w
	    else:
	        if s != '':
	            text_lst.append(s)
	        s = ''
	text_lst.append(s)
	result_word = []
	for elem in text_lst:
	    word = ''
	    min_dist = float('inf')
	    for s in rc.class3:
	        s = ' '.join([w for w in s.lower().split() if w not in stop_words])

	        dist3 = textdistance.hamming(s, elem)
	        if dist3 < min_dist:
	            min_dist = dist3
	            word = s
	    result_word.append(word)
	        
	return result_word


def near_metrostation(lat, lon):
	data = pd.read_csv('metro.csv')
	min_dist = float('inf')
	indx = 300
	for i in range(len(data)):
	    cleveland_oh = (data['latitude'].iloc[i], data['longitude'].iloc[i])
	    dist = great_circle((lat, lon), cleveland_oh).km
	    if dist < min_dist:
	        min_dist = dist
	        indx = i
	return data['name'].iloc[indx]

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = bd.get_current_state(message.chat.id)
    if state == config.States.S_WISH.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал дать команду :( Жду...")
    elif state == config.States.S_NOTIFICATIONS.value:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить пункт назначения :( Жду...")
    elif state == config.States.S_SIGHTS.value:
        bot.send_message(message.chat.id, "Я до сих пор не знаю, где показывать развлекательные места :( Жду...")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Привет, меня зовут Сережа! Чем могу быть полезен? Я умею включать уведомления и показывать крутые места)")
        bd.set_state(message.chat.id, config.States.S_WISH.value)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Что ж, начнём по-новой. Чем могу быть полезен?")
    bd.set_state(message.chat.id, config.States.S_WISH.value)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    remove_button_geo = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Благодарю!",reply_markup=remove_button_geo)
    response = near_metrostation(lat, lon)
    bot.send_message(message.chat.id, "Ближайшая к Вам станция метро {}".format(response.title()))
    bot.edit_message_live_location(lat, lon, message.chat.id, message.message_id)
    bd.set_state(message.chat.id, config.States.S_NEW_START.value)

@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_NEW_START.value)
def user_entering_wish(message):
	text = message.text
	bot.send_message(message.chat.id, "Чем еще я могу Вам помочь? Напомню: Я умею включать уведомления и показывать крутые места)")

	bd.set_state(message.chat.id, config.States.S_WISH.value)


@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_WISH.value)
def user_entering_wish(message):
	text = message.text
	
	id_request = near_request(text)
	if id_request == 2:
		bot.send_message(message.chat.id, "Отлично! На какую станцию планируете поехать?")
		bd.set_state(message.chat.id, config.States.S_NOTIFICATIONS.value)
	elif id_request == 1:
		bot.send_message(message.chat.id, "Отлично! Показать места рядом с Вами или около конкретной станции метро?")
		bd.set_state(message.chat.id, config.States.S_SIGHTS.value)
	else:
		bot.send_message(message.chat.id, "Я Вас не совсем понял. Пожалуйста, укажите Ваши пожелания еще раз!")
		


@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_NOTIFICATIONS.value)
def user_notifications(message):
    text = define_station(message.text)
    bot.send_message(message.chat.id, 'Вы выбрали станцию метро' + ' ' + text.title() + ', да/нет?')
    bd.set_state(message.chat.id, config.States.S_YESNO.value)


@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_YESNO.value)
def user_notifications(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Замечательно!Укажите Ваши пожелания по маршруту(пересадки)")
        bd.set_state(message.chat.id, config.States.S_CHANGES.value)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, "Укажите станцию метро еще раз")
        bd.set_state(message.chat.id, config.States.S_NOTIFICATIONS.value)
    else:
        bot.send_message(message.chat.id, 'Напишите только да или нет!')

@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_CHANGES.value)
def user_notifications(message):
    ch= changes(message.text)
    if len(ch) != 0:
        bot.send_message(message.chat.id, "Вы хотите поехать через {}, да/нет?".format(','.join(list(map(lambda x: x.title(), ch)))))
        bd.set_state(message.chat.id, config.States.S_YESNO_NOTIF.value)
    else:
        bot.send_message(message.chat.id, 'Я Вас не совсем понял, укажите пересадки еще раз!')

@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_YESNO_NOTIF.value)
def user_notifications(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Отлично! Уведомления включены!")
        bd.set_state(message.chat.id, config.States.S_NEW_START.value)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, "Укажите пересадки еще раз!")
        bd.set_state(message.chat.id, config.States.S_CHANGES.value)
    else:
        bot.send_message(message.chat.id, 'Напишите только да или нет!')


@bot.message_handler(func=lambda message: bd.get_current_state(message.chat.id).decode('utf-8') == config.States.S_SIGHTS.value)
def user_sights(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    
    keyboard.add(button_geo)
    response = bot.send_message(message.chat.id, "Поделитесь Вашим местоположением!", reply_markup=keyboard)


if __name__ == "__main__":
    bot.polling(none_stop=True)


