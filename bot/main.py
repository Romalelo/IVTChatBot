import telebot
from telebot import types, TeleBot

from parser import parse_all_info
from config import TOKEN, DataFiles, ADMIN_PASSWORD
from utils import add_new_user, check_if_student_exists, set_student_id, check_if_registered, \
    get_student_marks_by_user_id, delete_student_id, get_users, get_formatted_output
from keyboards import main_keyboard, admin_keyboard, schedule_keyboard
from admin import check_user_is_admin, add_admin

bot = telebot.TeleBot(TOKEN)

admin_status = {}
user_status = {}


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте, это бот деканата ИВТ. Для начала использования введите номер студенческого билета.")
    user_id = message.chat.id
    add_new_user(user_id)


@bot.message_handler(func=lambda m: m.text == "Назад")
def get_student_marks_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Главное меню', parse_mode="HTML", reply_markup=main_keyboard)


@bot.message_handler(func=lambda m: m.text == "Мои Оценки")
def get_student_marks_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, get_student_marks_by_user_id(user_id), parse_mode="HTML", reply_markup=main_keyboard)


@bot.message_handler(func=lambda m: m.text == "Расписание")
def show_schedule_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Выберите какое расписание Вы хотите посмотреть', parse_mode="HTML",
                     reply_markup=schedule_keyboard)


@bot.message_handler(func=lambda m: m.text == "Посмотреть расписание группы")
def show_group_schedule_handler(message):
    user_id = message.chat.id
    user_status[user_id] = 'group'
    bot.send_message(user_id, f'Введите Вашу группу:')


@bot.message_handler(func=lambda m: m.text == "Посмотреть расписание преподавателей")
def show_professors_schedule_handler(message):
    user_id = message.chat.id
    user_status[user_id] = 'professors'
    bot.send_message(user_id, f'Введите ФИО профессора:')


@bot.message_handler(func=lambda m: m.text == "Посмотреть расписание аудитории")
def show_classroom_schedule_handler(message):
    user_id = message.chat.id
    user_status[user_id] = 'classrooms'
    bot.send_message(user_id, f'Введите номер аудитории:')


@bot.message_handler(func=lambda m: m.text == "Ввести номер номер студенческого билета заново")
def set_new_student_id_handler(message):
    user_id = message.chat.id
    no_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    no_keyboard.add(types.KeyboardButton(f"{delete_student_id(user_id)}"))
    delete_student_id(user_id)
    bot.send_message(message.chat.id, "Введите новый номер студенческого билета.", reply_markup=no_keyboard)


@bot.message_handler(func=lambda m: m.text == ADMIN_PASSWORD)
def enter_admin_panel_handler(message):
    user_id = message.chat.id
    add_admin(user_id)
    bot.send_message(user_id, f'Вы теперь администратор!')
    bot.send_message(user_id, 'Добро пожаловать в админ панель', reply_markup=admin_keyboard)


@bot.message_handler(func=lambda m: m.text == "admin")
def enter_admin_panel_handler(message):
    user_id = message.chat.id
    if check_user_is_admin(user_id):
        bot.send_message(user_id, 'Добро пожаловать в админ панель', reply_markup=admin_keyboard)


@bot.message_handler(func=lambda m: m.text == "Поменять ссылку на оценки (Яндекс Диск)")
def set_yandex_disk_link_handler(message):
    user_id = message.chat.id
    if check_user_is_admin(user_id):
        admin_status[user_id] = 'yandex_disk'
        bot.send_message(user_id, 'Введите новую ссылку для оценок на Яндекс Диск', reply_markup=admin_keyboard)


@bot.message_handler(func=lambda m: m.text == "Поменять ссылку на расписание (Google Sheets)")
def set_google_sheets_link_handler(message):
    user_id = message.chat.id
    if check_user_is_admin(user_id):
        admin_status[user_id] = 'google_sheets'
        bot.send_message(user_id, 'Введите новую ссылку для расписания на Google Sheets', reply_markup=admin_keyboard)


@bot.message_handler(func=lambda m: m.text == "Обновить оценки/расписание")
def set_google_sheets_link_handler(message):
    user_id = message.chat.id
    if check_user_is_admin(user_id):
        admin_status[user_id] = 'update'
        bot.send_message(user_id, 'Оценки обновлены', reply_markup=admin_keyboard)


@bot.message_handler(func=lambda m: m.text == "Рассылка ВСЕМ пользователям")
def set_google_sheets_link_handler(message):
    user_id = message.chat.id
    if check_user_is_admin(user_id):
        admin_status[user_id] = 'broadcast'
        bot.send_message(user_id, 'Введите сообщение для рассылки всем пользователям', reply_markup=admin_keyboard)


@bot.message_handler()
def other_message_handler(message):
    user_id = message.chat.id

    if check_user_is_admin(user_id) and admin_status[user_id]:
        try:
            if admin_status[user_id] == 'yandex_disk':
                parse_all_info(yandex_link=str(message.text))
            elif admin_status[user_id] == 'google_sheets':
                parse_all_info(google_link=str(message.text))
            elif admin_status[user_id] == 'update':
                parse_all_info()
            elif admin_status[user_id] == 'broadcast':
                for user in get_users():
                    try:
                        bot.send_message(user, message.text)
                    except Exception as e:
                        bot.send_message(user_id, f'Ошибка отправки пользователю {user}\n{e}')
        except Exception as e:
            bot.send_message(user_id, f'Ошибка {e}')
        else:
            bot.send_message(user_id, 'Успешно!')
        admin_status[user_id] = ''
        return

    if user_status.get(user_id, None):
        if user_status[user_id] == 'group':
            bot.send_message(user_id, get_formatted_output(DataFiles.GROUPS, message.text), parse_mode="HTML",
                             reply_markup=schedule_keyboard)
        elif user_status[user_id] == 'professors':
            bot.send_message(user_id, get_formatted_output(DataFiles.PROFESSORS, message.text), parse_mode="HTML",
                             reply_markup=schedule_keyboard)
        elif user_status[user_id] == 'classrooms':
            bot.send_message(user_id, get_formatted_output(DataFiles.CLASSROOMS, message.text), parse_mode="HTML",
                             reply_markup=schedule_keyboard)

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
