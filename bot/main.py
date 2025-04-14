import telebot
from telebot import types, TeleBot
import time
import threading
from config import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

# Клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.KeyboardButton(""))
main_keyboard.add(types.KeyboardButton(""))


settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.add(types.KeyboardButton(""))
settings_keyboard.add(types.KeyboardButton(""))
settings_keyboard.add(types.KeyboardButton(""))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте, это бот деканата ИВТ. Для начала использования введите номер студенческого билета.",
        reply_markup=main_keyboard
    )

