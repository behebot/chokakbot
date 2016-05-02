#!/usr/bin/python

import telebot
import logging
from random import randint

import config
import secure_config
from config import stickers
from timeofday import TimeOfDay
from giphy import Giphy


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(secure_config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, config.welcome_message)


@bot.message_handler(commands=['time'])
def time_cmd(message):
    if randint(1, 100) >= 90:
        bot.send_sticker(message.chat.id, stickers['adventure_time'])
    else:
        tod = TimeOfDay(config.users).get_time_of_day()
        bot.send_message(message.chat.id,
                         "Current time of day in Chatik is {}".format(tod))


@bot.message_handler(commands=['giphy'])
def giphy_cmd(message):
    giphy = Giphy(message.text.replace('/giphy ', ''))
    bot.send_message(message.chat.id, giphy.get_search_result())


@bot.message_handler(commands=['time_debug'])
def send_time_debug(message):
    tod = TimeOfDay(config.users, debug=True).get_time_of_day()
    msg = "Debug output for /time command:\n{}".format(tod)
    bot.send_message(message.chat.id, msg)


bot.polling(none_stop=False, interval=3)
