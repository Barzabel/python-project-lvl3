import pytest
import requests_mock
from page_loader.pageloader import  page_loader
import os
import tempfile


url_test = r'https://ru.hexlet.io/courses'
data = 'data'


def test_one():
    with tempfile.TemporaryDirectory() as tmp:
        with requests_mock.Mocker() as m:
            m.get(
                url_test,
                text=data
            )
            path_to_file = page_loader(
                url_test,
                tmp
            )			
            assert path_to_file == os.path.join(tmp, 'ru-hexlet-io-courses.html')
            with open(path_to_file, "r") as file:
                assert file.read() == data
