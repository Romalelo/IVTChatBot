from telebot import types

# Клавиатуры
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(types.KeyboardButton("Мои Оценки"))
main_keyboard.add(types.KeyboardButton("Расписание"))
main_keyboard.add(types.KeyboardButton("Ввести номер номер студенческого билета заново"))

# Админская клавиатура
admin_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(types.KeyboardButton('Поменять ссылку на оценки (Яндекс Диск)'),
                   types.KeyboardButton('Поменять ссылку на расписание (Google Sheets)'))
admin_keyboard.add(types.KeyboardButton('Обновить оценки/расписание'))
admin_keyboard.add(types.KeyboardButton('Рассылка ВСЕМ пользователям'))
admin_keyboard.add(types.KeyboardButton('Назад'))


schedule_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
schedule_keyboard.add(types.KeyboardButton('Посмотреть расписание группы'))
schedule_keyboard.add(types.KeyboardButton('Посмотреть расписание преподавателей'))
schedule_keyboard.add(types.KeyboardButton('Посмотреть расписание аудитории'))
schedule_keyboard.add(types.KeyboardButton('Назад'))
