.PHONY: run-server
run-server:
	poetry run python3 core/manage.py runserver

.PHONY: migrations
migrations:
	poetry run python3 core/manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python3 core/manage.py migrate

