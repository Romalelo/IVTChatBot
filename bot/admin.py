from utils import load_json, save_json
from config import DataFiles


def add_admin(user_id: int):
    """
    Добавляет пользователя в список администраторов, если он ещё не является админом.

    :param user_id: Telegram ID пользователя.
    """
    data = load_json(DataFiles.USERS_FILE.value)
    if user_id not in data.get('admins', []):
        data['admins'].append(user_id)
        save_json(data, DataFiles.USERS_FILE.value)


def delete_admin(user_id: int, user_to_delete_id: int):
    """
    Удаляет администратора, если вызывающий пользователь является админом.

    :param user_id: Telegram ID вызывающего пользователя.
    :param user_to_delete_id: Telegram ID админа, которого нужно удалить.
    """
    data = load_json(DataFiles.USERS_FILE.value)
    if check_user_is_admin(user_id) and user_to_delete_id in data.get('admins', []):
        data['admins'].remove(user_to_delete_id)
        save_json(data, DataFiles.USERS_FILE.value)


def get_admins() -> list:
    """
    Возвращает список ID администраторов из файла users.json.

    :return: Список ID админов.
    """
    data = load_json(DataFiles.USERS_FILE.value)
    return data['admins']


def check_user_is_admin(user_id) -> bool:
    """
    Возвращает True если пользователь является админом, иначе False

    :param user_id: ID пользователя
    :return:
    """
    data = get_admins()
    return user_id in data
