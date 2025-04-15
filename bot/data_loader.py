import requests
import os
from urllib.parse import urlencode
from zipfile import ZipFile
import pandas as pd
from utils import save_json

API_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

STUDENTS_FILE = '../data/jsons/students.json'


def download_students_marks_from_yandex_disk(url: str = 'https://disk.yandex.ru/d/DdP2kTZLhyfeVQ'):
    """
    Загрузка новых данных по студентам с Яндекс Диска для админки

    :param url: URL ссылка на Яндекс Диск
    :return:
    """
    try:
        final_url = API_URL + urlencode(dict(public_key=url))
        response = requests.get(final_url)
        download_url = response.json()['href']

        download_response = requests.get(download_url)
        with open('downloaded_file.zip', 'wb') as f:
            f.write(download_response.content)
        with ZipFile('downloaded_file.zip', 'r') as f:
            f.extractall('../data/xlsx')
        os.remove("downloaded_file.zip")
        parse_data_into_json()
        return f'Успешно!'
    except Exception as e:
        return f'Что-то пошло не так при загрузке файла с Яндекс Диска: {e}'


def parse_data_into_json():
    """
    Парсинг данных из папки xlsx в students.json

    :return:
    """
    data_xlsx_dir = '../data/xlsx'
    students_data_as_list = []
    students_data_as_dict = {}
    dir_list = os.listdir(data_xlsx_dir)

    try:
        for dir in dir_list:
            files_list = os.listdir(data_xlsx_dir + '/' + dir)
            for file in files_list:
                excel_reader = pd.ExcelFile(data_xlsx_dir + '/' + dir + '/' + file)
                sheet_to_df_map = {}
                for sheet_name in excel_reader.sheet_names:
                    sheet_to_df_map[sheet_name] = excel_reader.parse(sheet_name, index_col=0, skiprows=2)
                    students_data_as_list += (sheet_to_df_map[sheet_name].to_dict(orient="records"))

        for student in students_data_as_list:
            try:
                student_id = int(student.pop('Студенч. номер'))
            except:
                continue
            students_data_as_dict[student_id] = student
        save_json(students_data_as_dict, STUDENTS_FILE)
    except Exception as e:
        print(f'Ошибка: {e}')


download_students_marks_from_yandex_disk()
