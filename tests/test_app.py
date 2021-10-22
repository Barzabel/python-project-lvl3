import pytest
import requests_mock
from page_loader.pageloader import  page_loader
import os
import tempfile


adapter = requests_mock.Adapter()
url_test = 'https://ru.hexlet.io/courses'
data = 'data'
adapter.register_uri('GET', url_test, text=data)


def test_one():
	with tempfile.TemporaryDirectory() as tmp:
		path_to_file = page_loader(url_test, tmp)
		assert path_to_file == os.path.join(tmp, 'ru-hexlet-io-courses.html')
		