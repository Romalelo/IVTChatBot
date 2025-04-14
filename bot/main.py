import telebot
from telebot import types, TeleBot
import time
import threading
from config import API_TOKEN
from utils import add_new_user, check_if_student_exists, set_student_id, check_if_registered

bot = telebot.TeleBot(API_TOKEN)

# Клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.KeyboardButton("Оценки"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте, это бот деканата ИВТ. Для начала использования введите номер студенческого билета.")
    user_id = message.chat.id
    add_new_user(user_id)


@bot.message_handler(func=lambda m: m.text == "Оценки")
def get_student_marks(message):
    user_id = message.chat.id


@bot.message_handler()
def enter_student_id(message):
    user_id = message.chat.id
    if check_if_registered(user_id):
        return

    if message.content_type != 'text':
        bot.send_message(user_id, f"❗ Неверные данные! Пожалуйста, введите номер студенческого билета!")
    elif check_if_student_exists(message.text):
        bot.send_message(user_id, f"Успешно!")
        set_student_id(user_id, message.text)
    else:
        bot.send_message(user_id, f"Студент с таким номером не найден!")


bot.infinity_polling()
