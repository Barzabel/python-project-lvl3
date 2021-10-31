import pytest
import requests_mock
from page_loader.pageloader import  page_loader
import os
import tempfile, shutil


url_test = r'https://ru.hexlet.io/courses'
url_test_js = r"https://ru.hexlet.io/js/script.js"
url_test_css = r"https://ru.hexlet.io/static/style.css"
with open("tests/fixtures/test2/index.html", 'r') as file:
    data = file.read()
with open("tests/fixtures/test2/right_answer.html", 'r') as file:
    right_answer_data = file.read()
with open("tests/fixtures/test2/js/script.js", 'r') as file:
    js = file.read()
with open("tests/fixtures/test2/static/style.css", 'r') as file:
    css = file.read()

def test_name():
    with tempfile.TemporaryDirectory() as tmp:
        path_to_dir = os.path.join(tmp, 'ru-hexlet-io-courses_files')
        with requests_mock.Mocker() as mask_url:
            mask_url.get(
                url_test,
                text = data
            )
            mask_url.get(
                url_test_js,
                text = js
            )
            mask_url.get(
                url_test_css,
                text = css
            )
            path_to_file = page_loader(
                url_test,
                tmp
            )

            with open(path_to_file, "r") as file:
                assert file.read() == right_answer_data