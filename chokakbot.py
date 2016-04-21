#!/usr/bin/python

import telebot
import logging
from random import randint

import config
import secure_config
from config import stickers
from timeofday import TimeOfDay


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(secure_config.token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, config.welcome_message)


@bot.message_handler(commands=['time'])
def time_cmd(message):
    if randint(1, 100) >= 90:
        bot.send_sticker(message.chat.id, stickers['adventure_time'])
    else:
        tod = TimeOfDay(config.users).get_time_of_day()
        bot.reply_to(message,
                     "Current time of day in Chatik is {}".format(tod))


@bot.message_handler(commands=['time_debug'])
def send_time_debug(message):
    tod = TimeOfDay(config.users, debug=True).get_time_of_day()
    msg = "Debug output for /time command:\n{}".format(tod)
    bot.reply_to(message, msg)


@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "I don't know this command. Soryan.")


bot.polling(none_stop=True)
