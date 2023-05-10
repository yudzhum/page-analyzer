PORT ?= 8000
DB_NAME=pageanalyzer
DB_USER=yudzhum


install:
	poetry install

db-build:
	db-drop db-create schema-load

db-drop:
	dropdb $(DB_NAME)

db-create:
	createdb $(DB_NAME)

schema-load:
	psql $(DB_NAME) < database.sql

db-reset:
	dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

connect:
	psql -d $(DB_NAME)

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

dev:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_analyzer

