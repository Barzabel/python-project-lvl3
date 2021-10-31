import pytest
import requests_mock
from page_loader.pageloader import  page_loader
import os
import tempfile, shutil


url_test = r'https://ru.hexlet.io/courses'
url_test_img = r"https://ru.hexlet.iostatic/img/img1.png"
with open("tests/fixtures/test1/index.html", 'r') as file:
    data = file.read()

with open("tests/fixtures/test1/rigt_answer.html", 'r') as file:
    right_answer_data = file.read()


with open("tests/fixtures/test1/static/img/img1.png", 'rb') as file:
    img = file.read()


def test_name():
    with tempfile.TemporaryDirectory() as tmp:
        path_to_dir = os.path.join(tmp, 'ru-hexlet-io-courses_files')
        with requests_mock.Mocker() as mask_url:
            mask_url.get(
                url_test,
                text = data
            )
            mask_url.get(
                url_test_img,
                content = img 
            )
            path_to_file = page_loader(
                url_test,
                tmp
            )
            assert path_to_file == os.path.join(tmp, 'ru-hexlet-io-courses.html')
            assert os.path.exists(path_to_dir)


def test_data():
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as mask_url:
            mask_url.get(
                url_test,
                text = data
            )
            mask_url.get(
                url_test_img,
                content = img 
            )
            path_to_file = page_loader(
                url_test,
                tmp
            )
            with open(path_to_file, "r") as file:
                assert file.read() == right_answer_data
