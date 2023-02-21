MANAGE := poetry run python manage.py

install:
	poetry install

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

PORT ?= 8000
start:
	python manage.py migrate
	poetry run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi

dev:
	$(MANAGE) runserver

lint:
	poetry run flake8 task_manager

selfcheck:
	poetry check

test:
	$(MANAGE) test

check: selfcheck lint test

test-coverage:
	poetry run coverage run ./manage.py test
	poetry run coverage report
	poetry run coverage xml

.PHONY: shell
shell:
	$(MANAGE) shell_plus --ipython
