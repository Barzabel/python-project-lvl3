import os


def criet_name(url):
    pass


def safe_data(data, name, path_output):
    return os.join(path_output, name)


def gat_data(url):
    pass


def page_loader(url, path_output):
    data = gat_data(url)
    name = criet_name(url)
    path_to_file = safe_data(data, name, path_output)
    return path_to_file