install: #poetry install
	poetry install;

build:
	rm -rf dist
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

all_tests:
	poetry run pytest

.PHONY: build lint package-install test