import os
import re
import requests
from bs4 import BeautifulSoup


def criet_name(url, type_file='dir'):
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
    if len(name) > 49:
        name = "{}{}{}".format(
            name[:5], name[len(name) // 2: len(name) // 2 + 5],
            name[:-5])
    if type_file == "dir":
        name = '{}_files'.format(name)
    elif type_file == "html":
        name = '{}.html'.format(name)
    elif type_file == "png":
        name = '{}.png'.format(name)
    return name


def safe_data(name, data='', path_output='', type_file='html'):
    path = os.path.join(os.getcwd(), path_output)
    path_to_file = os.path.join(path, name)

    if type_file == 'html':
        with open(path_to_file, 'w') as file:
            file.write(data)
        return path_to_file
    elif type_file == 'dir':
        try:
            os.mkdir(path_to_file)
            return path_to_file
        except FileExistsError:
            return path_to_file
    elif type_file == 'img':
        with open(path_to_file, "wb") as file:
            file.write(data)

        relative_file_path_img = re.search(
            r'[^\/]*\/[^\/]*\.png',
            path_to_file
            ).group()
        return relative_file_path_img


def gat_data(url, type_file='html'):
    if type_file == 'html':
        return requests.get(url).text
    elif type_file == 'img':
        return requests.get(url).content


def load_img_in_html(url, path_output, path_html):
    name = criet_name(url, type_file='dir')
    name_html = os.path.basename(path_html)
    path_to_dir = safe_data(
        name=name,
        path_output=path_output,
        type_file='dir'
    )
    get_index_url = re.match(r'.*:\/\/.*?\/', url)
    clear_url = get_index_url.group(0)

    with open(path_html, "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    for tag in soup.find_all("img"):
        if re.match(r'.*:\/\/', tag['src']) is None:
            url_img = "{}{}".format(clear_url[:-1], tag['src'])
        else:
            url_img = tag['src']

        data_img = gat_data(url_img, type_file='img')
        name_img = criet_name(url_img, type_file='png')
        new_src = safe_data(
            name=name_img,
            data=data_img,
            path_output=path_to_dir,
            type_file='img'
        )
        tag['src'] = new_src
    safe_data(
        name_html,
        data=soup.prettify(),
        path_output=path_output,
        type_file='html'
    )
    return True


def page_loader(url, path_output):
    data = gat_data(url)
    name = criet_name(url, 'html')
    path_to_file = safe_data(
        name,
        data=data,
        path_output=path_output
    )
    load_img_in_html(url, path_output, path_to_file)
    return path_to_file
