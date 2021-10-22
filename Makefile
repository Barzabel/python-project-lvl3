install: #poetry install
	poetry install;

build:
	poetry build;

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff;

all_tests:
	poetry run pytest;