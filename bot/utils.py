import json

USERS_FILE = '../data/jsons/users.json'
STUDENT_FILE = '../data/jsons/students.json'


def load_json(file: str) -> dict:
    """
    Загружает данные из файла .json

    :param file: Путь к файлу
    :return: Данные из .json в виде dict
    """
    with open(file, 'r') as f:
        return json.load(f)


def save_json(data, file: str) -> None:
    """
    Сохраняет данные в файле .json

    :param data: Данные, которые надо сохранить
    :param file: Путь к файлу
    :return:
    """
    with open(file, 'w', encoding='utf-8') as f:
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


def delete_student_id(user_id: int) -> int | None:
    """
    Удаляет пару user_id: student_id в файле users.json

    :param user_id:
    :return:
    """
    user_data = load_json(USERS_FILE)
    if str(user_id) not in user_data['user_student'].keys():
        return None
    student_id = user_data['user_student'].pop(str(user_id))
    save_json(user_data, USERS_FILE)
    return student_id


def add_new_user(user_id: int) -> None:
    """
    Добавляет нового пользователя в файл users.json

    :param user_id:
    :return:
    """
    user_data = load_json(USERS_FILE)
    if user_id not in user_data['users']:
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


def get_student_marks_by_user_id(user_id: int) -> str:
    """
    Возвращает красиво отформатированную информацию о результатах студента для Telegram (HTML-разметка)

    :param user_id: Id пользователя в телеграм
    :return: Информация о результатах студента string
    """
    student_id = load_json(USERS_FILE)['user_student'][str(user_id)]
    student_marks = load_json(STUDENT_FILE)[student_id]

    result_lines = ['<b>📋 Результаты по предметам:</b>']
    for subject, mark in student_marks.items():
        display_mark = ''
        if subject == 'Примечание':
            continue

        is_starred = '*' in str(mark)
        mark_clean = str(mark).replace('*', '').replace('/', '').rstrip()

        if isinstance(mark, str) and mark_clean.lower() in ['незач', 'незачет', 'не зачтено']:
            display_mark = '❌'
        elif isinstance(mark, str) and mark_clean.lower() in ['зач', 'зачтено']:
            display_mark = '✅'
        elif isinstance(mark, str) and mark_clean.lower() in ['неяв', 'неявка']:
            display_mark = 'неявка'
        elif mark_clean.isdigit():
            display_mark = mark_clean
        elif display_mark:
            display_mark = mark_clean

        display_mark += '*' if is_starred else ''

        # Каждую строку оборачиваем в <code>
        result_lines.append(f'<code>{subject[:28]:28}: {display_mark}</code>')

    note = student_marks.get('Примечание', '').strip() if type(student_marks.get('Примечание', '')) == str else ''
    if note:
        result_lines.append(f'\n<b>📌 Примечание:</b> <i>{note}</i>')

    return '\n'.join(result_lines)
