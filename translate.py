import requests
from datetime import datetime


def reader():
    file = input('Введите название файла, из которого будем брать текст:\n>')
    with open(file, encoding='utf8') as data:
        text = data.read()
    from_lang = input('С какого языка переводить? (de, ru, es...)\n>').lower()
    to_lang = input('На какой язык переводим?\n>').lower()
    result_name = f'result-{from_lang}-{to_lang}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt'
    with open(result_name, 'w', encoding='utf8') as result:
        translated_text = translate_it(text, from_lang, to_lang)
        result.write(translated_text)
    print(f'Результат перевода:\n{translated_text}')
    return result_name


def translate_it(text, from_lang, to_lang):
    api_key = 'your_token_here'
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
    token = 'OAuth your_token_here'
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
