import telebot
from telebot import types, TeleBot
import time
import threading
from config import API_TOKEN
from utils import add_new_user

bot = telebot.TeleBot(API_TOKEN)

# Клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.KeyboardButton("Начать регистрацию заново"))

settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.add(types.KeyboardButton(""))
settings_keyboard.add(types.KeyboardButton(""))
settings_keyboard.add(types.KeyboardButton(""))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Здравствуйте, это бот деканата ИВТ. Для начала использования введите ФИО студента.",
        reply_markup=main_keyboard
    )
    user_id = message.chat.id
    add_new_user(user_id)


@bot.message_handler()
def enter_username(message):
    user_id = message.chat.id
    if message.content_type != 'text':
        bot.send_message(user_id, f"❗ Неверные данные! Пожалуйста, введите ФИО студента")
    else:
        bot.send_message(user_id, f"❗ Пожалуйста, введите ФИО студента")


bot.infinity_polling()
