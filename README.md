# Marketing Lead Helper Tool

#TODO Describe project

## Technologies
- Python 3.11
- FastAPI==0.109.0
- Postgres 14.6
- Uvicorn
- Docker

## Setup
Please, follow steps to prepare project for local development:
1. Clone repository.
2. Setup venv with Python 3.11.
3. Install dependencies from requirements.txt file.
4. Create `.env` file from `.env.example`.
5. Setup database: `docker compose up -d`
6. Run migrations: `alembic upgrade head`
7. Initialise basic data: `python -m src.scripts.init_db`
8. Install pre-commit hooks: `pre-commit install`
9. Run `uvicorn src.main:app --reload`

## Migrate database
1. Initialize migrations: `alembic revision --autogenerate -m "init"`
2. Make migrations: `alembic revision -m "<MSG>"`
3. Run migrations: `alembic upgrade head`

## APIs
1. Swagger: `http://127.0.0.1:8000/docs`
2. TODO
