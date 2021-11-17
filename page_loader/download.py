import os
import re
import requests
from bs4 import BeautifulSoup
from page_loader.logger import get_logger


logger = get_logger(__name__)


def is_dir_exist(output_dir):
    '''    Check is directory exist
    :param
        output_dir: directory path
    :return: True of False    '''
    return os.path.exists(output_dir) and os.path.isdir(output_dir)


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
    elif type_file == "img":
        name = '{}.png'.format(name[:-4])
    elif type_file == "js":
        name = '{}.js'.format(name[:-3])
    elif type_file == "css":
        name = '{}.css'.format(name[:-4])
    logger.info('making page_file_name or page_file_path {}'.format(name))
    return name


def safe_data(name, data='', path_output='', type_file='html'):
    logger.info('start safe_data with name={}, path_output={}, type_file={}\
        '.format(
            name,
            path_output,
            type_file
        ))

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
    elif type_file == 'css':
        with open(path_to_file, "w") as file:
            file.write(data)
        relative_file_path_img = re.search(
            r'[^\/]*\/[^\/]*\.css',
            path_to_file
            ).group()
        return relative_file_path_img
    elif type_file == 'js':
        with open(path_to_file, "w") as file:
            file.write(data)
        relative_file_path_img = re.search(
            r'[^\/]*\/[^\/]*\.js',
            path_to_file
            ).group()
        return relative_file_path_img


def get_data(url, type_file='html'):
    try:
        req_data = requests.get(url)
        if req_data.status_code > 299:
            logging.exception("get_data url {}, status {}".format(url, req_data.status_code))
        if type_file == 'html':
            return req_data.text
        elif type_file == 'img':
            return req_data.content
        elif type_file == 'js' or type_file == 'css':
            return req_data.text

    except e:
        logging.exception("get_data url {}, type_file{}".format(url, type_file))


def load_in_html(url, path_output, path_html):
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

    def _find_and_save_data(tag, type_file, atr='src'):
        for tag in soup.find_all(tag):
            val = tag.get(atr)
            if val is not None and re.match(r'.*:\/\/', val) is None:
                if type_file == 'css' and tag.get('rel') != ['stylesheet']:
                    continue
                url = "{}{}".format(clear_url[:-1], tag[atr])
            else:
                continue

            data = get_data(url, type_file=type_file)
            name = criet_name(url, type_file=type_file)
            new_src = safe_data(
                name=name,
                data=data,
                path_output=path_to_dir,
                type_file=type_file
            )
            tag[atr] = new_src
    _find_and_save_data(tag='img', type_file='img')
    _find_and_save_data(tag='link', type_file='css', atr='href')
    _find_and_save_data(tag='script', type_file='js')

    safe_data(
        name_html,
        data=soup.prettify(),
        path_output=path_output,
        type_file='html'
    )
    return True


def download(url, path_output):
    logger.info('start func with pageurl:{}, output_dir:{}\
        '.format(url, path_output))
    if not is_dir_exist(path_output):
        logger.warning("An output directory doesn't exist!")
        raise NameError('Missing directory')

    data = get_data(url)
    name = criet_name(url, 'html')
    path_to_file = safe_data(
        name,
        data=data,
        path_output=path_output
    )
    logger.info('html with local links saved')
    load_in_html(url, path_output, path_to_file)
    return path_to_file
