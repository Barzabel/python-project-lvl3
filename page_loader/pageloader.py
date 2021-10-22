import os
import re
import requests


def criet_name(url):
    """Берется адрес страницы без схемы
    Все символы, кроме букв и цифр, заменяются на дефис -.
    В конце ставится .html
    https://ru.hexlet.io/courses
    ru-hexlet-io-courses.html"""
    name = url
    shema = re.compile(r'.*://')
    change = re.compile(r'[^A-Za-z0-9]')
    name = shema.sub('', name, count=1)
    name = change.sub('-', name)
    name = '{}.html'.format(name)
    return name


def safe_data(data, name, path_output):
    path = os.path.join(os.getcwd(), path_output)
    path_to_file = os.path.join(path, name)
    with open(path_to_file, 'w') as file:
        file.write(data)
    return os.path.join(path, name)


def gat_data(url):
    return requests.get(url).text


def page_loader(url, path_output):
    data = gat_data(url)
    name = criet_name(url)
    path_to_file = safe_data(data, name, path_output)
    return path_to_file
