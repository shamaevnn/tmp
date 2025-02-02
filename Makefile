include .env
export


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
	docker compose up --build
