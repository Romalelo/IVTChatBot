import telebot
from telebot import types, TeleBot
from config import API_TOKEN
from utils import add_new_user, check_if_student_exists, set_student_id, check_if_registered, \
    get_student_marks_by_user_id, delete_student_id

bot = telebot.TeleBot(API_TOKEN)

# Клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.KeyboardButton("Мои Оценки"))
main_keyboard.add(types.KeyboardButton("Ввести номер номер студенческого билета заново"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте, это бот деканата ИВТ. Для начала использования введите номер студенческого билета.")
    user_id = message.chat.id
    add_new_user(user_id)


@bot.message_handler(func=lambda m: m.text == "Мои Оценки")
def get_student_marks(message):
    user_id = message.chat.id
    bot.send_message(user_id, get_student_marks_by_user_id(user_id), parse_mode="HTML", reply_markup=main_keyboard)


@bot.message_handler(func=lambda m: m.text == "Ввести номер номер студенческого билета заново")
def set_new_student_id(message):
    user_id = message.chat.id
    no_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    no_keyboard.add(types.KeyboardButton(f"{delete_student_id(user_id)}"))
    delete_student_id(user_id)
    bot.send_message(message.chat.id, "Введите новый номер студенческого билета.", reply_markup=no_keyboard)


@bot.message_handler()
def enter_student_id(message):
    user_id = message.chat.id
    if check_if_registered(user_id):
        bot.send_message(user_id, f"Неизвестная команда.", reply_markup=main_keyboard)
        return

    if message.content_type != 'text':
        bot.send_message(user_id, f"Неверные данные! Пожалуйста, введите номер студенческого билета!")
    elif check_if_student_exists(message.text):
        bot.send_message(user_id, f"Успешно!", reply_markup=main_keyboard)
        set_student_id(user_id, message.text)
    else:
        bot.send_message(user_id, f"Студент с таким номером не найден! Попробуйте ещё раз.")


bot.infinity_polling()
