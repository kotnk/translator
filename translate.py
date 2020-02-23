import requests
import os
from datetime import datetime


def reader():
    file = input('Введите путь файла, из которого будем брать текст:\n>')
    path = os.path.join(file)
    print(path, 'test')
    with open(path, encoding='utf8') as data:
        text = data.read()
    from_lang = input('С какого языка переводить? (de, ru, es...)\n>').lower()
    to_lang = input('На какой язык переводим?\n>').lower()
    result_path = input('Введите путь, куда сохранить файл: ')
    result_name = f'result-{from_lang}-{to_lang}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
    full_path = os.path.join(result_path, result_name)
    print(full_path, 'test')
    with open(full_path, 'w', encoding='utf8') as result:
        translated_text = translate_it(text, from_lang, to_lang='ru')
        result.write(translated_text)
    print(f'Результат перевода:\n{translated_text}')
    return full_path


def translate_it(text, from_lang, to_lang):
    api_key = 'trnsl.1.1.20200222T173117Z.44c78eecca664b79.27fcef98acd8ece997fa0520fec7fa6f081291f1'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    params = {
        'key': api_key,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang),
    }

    response = requests.get(url, params=params)
    json_ = response.json()
    try:
        return ''.join(json_['text'])
    except KeyError:
        print('Возникла проблема с текстом, возможно неверно были переданы параметры языка\n')
        reader()


def uploader(file):
    token = 'OAuth AgAAAAAgRZ8KAADLW-EJI3AA-EswnWkq2QpgWDo'
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
        'Authorization': token
    }
    params = {
        'path': f'{file}',
        'overwrite': 'False'
    }

    response = requests.get(url, headers=headers, params=params)
    upload_url = response.json()['href']
    with open(file, encoding='utf8') as text:
        data = text.read().encode('utf8')
        result = requests.put(upload_url, data=data)
        result_descriptor(result.status_code)


def result_descriptor(code):
    if code == 201:
        print('Загрузка успешно завершена!')
    elif code == 500 or 503:
        print('Ошибка сервера')
    elif code == 202:
        print('Файл успешно загружен и скоро появится на сервере')
    elif code == 507:
        print('Недостаточно места на диске')


if __name__ == '__main__':
    file = reader()
    print('>>>Инициализация загрузки...')
    uploader(file)
