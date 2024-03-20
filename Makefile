include .env
export


services:
	docker compose -f docker-compose.services.yml up --build

test_services:
	docker compose -f docker-compose.test.yml up --build

makemigrations:
	PYTHONPATH=. alembic revision -m "${m}" --autogenerate

migrate:
	PYTHONPATH=. alembic upgrade head

downgrade:
	PYTHONPATH=. alembic downgrade head-1

dev:
	uvicorn main:socket_app --host 0.0.0.0 --port 80 --reload

run_tests:
	pytest -v -s --color=yes --cov=app --cov-report term:skip-covered --timeout=30 --log-level=INFO tests/

up:
	docker compose -f docker-compose.server.yml up --build
