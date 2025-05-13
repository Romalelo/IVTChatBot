import os
from dotenv import load_dotenv
from enum import Enum


# Enum для путей к файлам
class DataFiles(Enum):
    SCHEDULE_FILE = '../data/jsons/schedule_file.xlsx'
    USERS_FILE = '../data/jsons/users.json'
    STUDENTS_FILE = '../data/jsons/students.json'
    GROUPS = '../data/jsons/schedule_by_groups.json'
    CLASSROOMS = '../data/jsons/classrooms.json'
    PROFESSORS = '../data/jsons/professors.json'


# Загрузка переменных окружения из файла .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
dotenv_path = os.path.normpath(dotenv_path)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# API Яндекс диска
API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
# Токен бота
TOKEN = os.getenv("TOKEN")
# Ссылка на таблицу с расписанием в формате "https://docs.google.com/spreadsheets/d/*id*/..."
GOOGLE_DRIVE_URL = os.getenv("GOOGLE_DRIVE_URL")
# Ссылка на Яндекс диск с оценками в формате "https://disk.yandex.ru/*id*"
YANDEX_DRIVE_URL = os.getenv("YANDEX_DRIVE_URL")
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')