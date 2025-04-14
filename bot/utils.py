import json

USERS_FILE = '../data/jsons/users.json'
STUDENT_FILE = '../data/jsons/students.json'


def load_json(file: str) -> dict:
    """
    Загружает данные из файла .json

    :param file: Название файла
    :return: Данные из .json
    """
    with open(file, "r") as f:
        return json.load(f)


def save_json(data, file: str) -> None:
    """
    Сохраняет данные в файле .json

    :param data: Данные, которые надо сохранить
    :param file: Название файла .json
    :return:
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def set_student_id(user_id: int, student_id: int) -> None:
    """
    Создаёт или изменяет пару user_id: student_id в файле users.json

    :param user_id: Id пользователя телеграм
    :param student_id: Номер студенческого билета
    :return:
    """
    if not check_if_student_exists(student_id):
        return
    user_data = load_json(USERS_FILE)
    user_data['user_student'][str(user_id)] = str(student_id)
    save_json(user_data, USERS_FILE)


def add_new_user(user_id: int) -> None:
    """
    Добавляет нового пользователя в файл users.json

    :param user_id:
    :return:
    """
    user_data = load_json(USERS_FILE)
    user_data['users'].append(user_id)
    save_json(user_data, USERS_FILE)


def check_if_student_exists(student_id: int) -> bool:
    """
    Проверяет существует ли такой студент вообще

    :param student_id:
    :return:
    """
    data = load_json(STUDENT_FILE)
    return str(student_id) in list(data.keys())


def check_if_registered(user_id: int) -> bool:
    """
    Проверяет зарегистрирован ли такой пользователь

    :param user_id:
    :return:
    """
    data = load_json(USERS_FILE)
    return str(user_id) in list(data['user_student'].keys())

