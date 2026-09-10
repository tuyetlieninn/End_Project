# My Project Backend

An internal project management backend built with FastAPI, asynchronous SQLAlchemy, and Alembic.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the Swagger UI at `http://127.0.0.1:8000/docs`.

## Main API Endpoints

- `POST /auth/register`: Register a new account.
- `POST /auth/login`: Log in and receive a JWT.
- `GET/POST /projects`: List and create projects for the current user.
- `GET/POST /tech-tags`: List and create technology tags.
- `GET /health`: Check service availability.

SQLite is used by default for development. Configure the database settings in `.env` when connecting to PostgreSQL.

## Migration

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
