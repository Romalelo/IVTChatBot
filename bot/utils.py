import json
from config import DataFiles
from typing import Literal


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
    user_data = load_json(DataFiles.USERS_FILE.value)
    user_data['user_student'][str(user_id)] = str(student_id)
    save_json(user_data, DataFiles.USERS_FILE.value)


def delete_student_id(user_id: int) -> int | None:
    """
    Удаляет пару user_id: student_id в файле users.json

    :param user_id:
    :return:
    """
    user_data = load_json(DataFiles.USERS_FILE.value)
    if str(user_id) not in user_data['user_student'].keys():
        return None
    student_id = user_data['user_student'].pop(str(user_id))
    save_json(user_data, DataFiles.USERS_FILE.value)
    return student_id


def add_new_user(user_id: int) -> None:
    """
    Добавляет нового пользователя в файл users.json

    :param user_id:
    :return:
    """
    user_data = load_json(DataFiles.USERS_FILE.value)
    if user_id not in user_data['users']:
        user_data['users'].append(user_id)
        save_json(user_data, DataFiles.USERS_FILE.value)


def check_if_student_exists(student_id: int) -> bool:
    """
    Проверяет существует ли такой студент вообще

    :param student_id:
    :return:
    """
    data = load_json(DataFiles.STUDENTS_FILE.value)
    return str(student_id) in list(data.keys())


def check_if_registered(user_id: int) -> bool:
    """
    Проверяет зарегистрирован ли такой пользователь

    :param user_id:
    :return:
    """
    data = load_json(DataFiles.USERS_FILE.value)
    return str(user_id) in list(data['user_student'].keys())


def get_student_marks_by_user_id(user_id: int) -> str:
    """
    Возвращает красиво отформатированную информацию о результатах студента для Telegram (HTML-разметка)

    :param user_id: Id пользователя в телеграм
    :return: Информация о результатах студента string
    """
    student_id = load_json(DataFiles.USERS_FILE.value)['user_student'][str(user_id)]
    student_marks = load_json(DataFiles.STUDENTS_FILE.value)[student_id]

    result_lines = ['<b>📋 Результаты по предметам:</b>']
    for subject, mark in student_marks.items():
        display_mark = ''
        if subject == 'Примечание':
            continue

        is_starred = '*' in str(mark)
        mark_clean = str(mark).replace('*', '').replace('/', '').rstrip()

        if isinstance(mark, str) and mark_clean.lower() in ['незач', 'незачет', 'не зачтено', 'неатт', 'неатт.',
                                                            'не атт']:
            display_mark = '❌'
        elif isinstance(mark, str) and mark_clean.lower() in ['зач', 'зачтено', 'атт', 'атт.', 'ат', 'ат.']:
            display_mark = '✅'
        elif isinstance(mark, str) and mark_clean.lower() in ['неяв', 'неявка', 'н/а', 'на']:
            display_mark = 'н'
        elif mark_clean.isdigit():
            display_mark = mark_clean
        elif display_mark == '':
            display_mark = mark_clean

        display_mark += '*' if is_starred else ''

        # Каждую строку оборачиваем в <code>
        result_lines.append(f'<code>{subject[:28]:28}: {display_mark}</code>')

    note = student_marks.get('Примечание', '').strip() if type(student_marks.get('Примечание', '')) == str else ''
    if note:
        result_lines.append(f'\n<b>📌 Примечание:</b> <i>{note}</i>')

    return '\n'.join(result_lines)


def get_users():
    data = load_json(DataFiles.USERS_FILE.value)
    return data['users']


def get_schedule_groups(filename: str = DataFiles.GROUPS.value) -> list:
    """Возвращает список доступных в расписании групп

    Args:
        filename (str, optional): Путь к файлу с расписанием по группам. Defaults to DataFiles.GROUPS.value.

    Returns:
        list: Список групп
    """
    groups = []
    file = load_json(filename)
    for group in file:
        groups.append(group['group_name'])
    return groups


def get_schedule_classrooms(filename: str = DataFiles.CLASSROOMS.value) -> list:
    """Возвращает список доступных в расписании аудиторий

    Args:
        filename (str, optional): Путь к файлу с расписанием по аудиториям. Defaults to DataFiles.CLASSROOMS.value.

    Returns:
        list: Список аудиторий
    """
    classrooms = []
    file = load_json(filename)
    for classroom in file:
        classrooms.append(classroom['classroom'])
    return classrooms


def get_schedule_professors(filename: str = DataFiles.PROFESSORS.value) -> list:
    """Возвращает список доступных в расписании преподавателей

    Args:
        filename (str, optional): Путь к файлу с расписанием по преподавателям. Defaults to DataFiles.PROFESSORS.value.

    Returns:
        list: Список преподавателей
    """
    professors = []
    file = load_json(filename)
    for professor in file:
        professors.append(professor['professor'])
    return professors


def format_schedule(schedule_obj: dict) -> str:
    """Форматирует недельное расписание

    Args:
        schedule_obj (dict): Объект, соответствующий группе, аудитории, преподавателю

    Returns:
        str: Недельное расписание
    """
    result = []

    # Проходим по каждому дню недели
    for day_info in schedule_obj['subjects']:
        day = day_info['day']
        subjects = day_info['subjects']

        result.append(f"{day.capitalize()}:\n")

        # Создаем таблицу для текущего дня
        table = []
        current_class = None

        for subject in subjects:
            class_num = subject['class']
            subject_name = subject['subject'].strip().replace('\n', ' ')
            numerator = subject['numerator']
            denominator = subject['denominator']
            common = subject['common']

            if common:
                # Если предмет общий, добавляем его в таблицу
                table.append(f"{class_num}: {subject_name}")
            elif numerator:
                # Если предмет идет по числителю
                if current_class == class_num:
                    table[-1] += f" / {subject_name} (числитель)"
                else:
                    table.append(f"{class_num}: {subject_name} (числитель)")
                current_class = class_num
            elif denominator:
                # Если предмет идет по знаменателю
                if current_class == class_num:
                    table[-1] += f" / {subject_name} (знаменатель)"
                else:
                    table.append(f"{class_num}: {subject_name} (знаменатель)")
                current_class = class_num

        # Добавляем сформированную таблицу в результат
        result.append("\n".join(table) + "\n")

    return "\n".join(result)


def get_formatted_output(filename: Literal[DataFiles.GROUPS, DataFiles.CLASSROOMS, DataFiles.PROFESSORS],
                         search_str: str) -> str:
    """Возвращает форматированный вывод расписания

    Args:
        filename: Тип файла (группы, аудитории, преподаватели)
        search_str (str): Строка для поиска

    Returns:
        str: Форматированный вывод расписания
    """
    file = load_json(filename.value)
    if filename == DataFiles.GROUPS:
        group_name = search_str
        group_obj = next((obj for obj in file if obj.get('group_name') == group_name), None)
        if group_obj is None:
            return "Группа не найдена"
        schedule = format_schedule(group_obj)
        return f"Расписание группы: {group_name}\n\n" + schedule
    elif filename == DataFiles.CLASSROOMS:
        classroom_name = search_str
        classroom_obj = next((obj for obj in file if obj.get('classroom') == search_str), None)
        if classroom_obj is None:
            return "Аудитория не найдена"
        schedule = format_schedule(classroom_obj)
        description = classroom_obj['description']
        return f"Расписание для аудитории: {classroom_name}\nОписание: {description}\n\n" + schedule
    elif filename == DataFiles.PROFESSORS:
        professor_name = search_str
        professor_obj = next((obj for obj in file if obj.get('professor') == search_str), None)
        if professor_obj is None:
            return "Преподаватель не найден"
        schedule = format_schedule(professor_obj)
        return f"Расписание преподавателя: {professor_name}\n\n" + schedule
    else:
        return "Произошла ошибка"
