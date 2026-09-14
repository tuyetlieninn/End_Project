

# End_Project Backend

Internal project performance management backend for the Project Management System, built with FastAPI, asynchronous SQLAlchemy, Alembic, and SQLite.

## Quick Start

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

Open the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Run Tests

```bash
python -m pytest tests/ -v
```

## API Endpoints

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/auth/register` | No | Register a new account. The default role is `member`. |
| POST | `/auth/login` | No | Log in and receive an `idToken`. |
| GET | `/projects` | Yes | List projects with pagination, search, and filters. |
| POST | `/projects` | Yes | Create a project. `created_by` is taken from the JWT. |
| GET | `/projects/{id}` | Yes | Get project details. Returns `404` for missing or soft-deleted projects. |
| PUT | `/projects/{id}` | Yes | Replace a project. Returns `404` for missing or soft-deleted projects. |
| DELETE | `/projects/{id}` | Yes | Soft-delete a project by setting `deleted_at`. |
| GET | `/tech-tags?q=` | Yes | Autocomplete technology tags with case-insensitive search. |

All endpoints except `/auth/*` and `/health` require a valid JWT in the `Authorization: Bearer <idToken>` header.

## Demo Flow

1. Call `POST /auth/register` and receive an `idToken`.
2. Call `POST /projects` with `technologies`, `project_types`, and `dev_process_phases` arrays.
3. Call `GET /projects?q=...&technology=...&page=1&page_size=20`.
4. Call `GET /tech-tags?q=py` for technology autocomplete.
5. Call `PUT /projects/{id}` to update a project.
6. Call `DELETE /projects/{id}` to soft-delete a project.

## Project Structure

```text
app/
├── main.py
├── core/          # Configuration, security, and password hashing
├── db/            # Database engine and session
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
├── api/routers/   # FastAPI routes
└── utils/         # CSV helpers and technology-tag upsert
tests/             # Pytest tests
```

SQLite is used by default for development. The database file `end_project.db` is created automatically on startup.


