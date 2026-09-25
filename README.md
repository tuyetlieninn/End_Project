# End_Project Backend

FastAPI backend for the project management system. It uses asynchronous SQLAlchemy, SQLite, Alembic, JWT authentication, and Pydantic validation.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in the backend directory:

```env
SECRET_KEY=replace-with-a-long-random-secret
DATABASE_URL=sqlite+aiosqlite:///./project.db
```

Apply the database migrations before starting the server:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Useful URLs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## Tests

```bash
python -m pytest tests/ -v
```

The test fixture creates an isolated SQLite schema for each test. Production and development schemas are managed by Alembic, not by application startup.

## API Overview

All routes except `/auth/register`, `/auth/login`, and `/health` require:

```text
Authorization: Bearer <idToken>
```

| Method | Path | Description |
| --- | --- | --- |
| POST | `/auth/register` | Register a user and return an id token. |
| POST | `/auth/login` | Authenticate a user and return an id token. |
| GET | `/projects` | List active projects with search, filters, and pagination. |
| POST | `/projects` | Create a project. `created_by` comes from the authenticated user. |
| GET | `/projects/{project_id}` | Get one active project. |
| PUT | `/projects/{project_id}` | Replace one active project. |
| DELETE | `/projects/{project_id}` | Soft-delete one active project. |
| GET | `/tech-tags?q=<text>` | Return up to 20 matching technology tag names. |
| POST | `/tech-tags` | Create a normalized technology tag. Duplicate names return `409`. |

There are no legacy project routers or duplicate model implementations. The active API is registered from `app/api/routers/auth.py`, `projects.py`, and `tags.py`.

## POST /projects

Create a project with the authenticated user's email stored in `created_by`.

Request:

```json
{
  "customer_name": "ABC Corporation",
  "project_name": "Payment Platform",
  "description": "Payment processing system",
  "start_date": "2026-04-01",
  "end_date": "2026-09-30",
  "is_ongoing": false,
  "team_size": 6,
  "total_man_month": 18.5,
  "source_note": "Customer interview",
  "industry": "Finance",
  "outcome_note": "Reduced manual reconciliation",
  "team_composition_note": "Backend, frontend, QA",
  "technologies": ["python", "fastapi", "postgresql"],
  "project_types": ["new_dev"],
  "dev_process_phases": ["requirements", "design", "implementation", "testing"]
}
```

Validation rules:

- `customer_name`, `project_name`, and `start_date` are required.
- Dates must be real dates in `YYYY-MM-DD` format.
- `end_date` must be on or after `start_date`.
- `end_date` must be omitted when `is_ongoing` is `true`.
- `team_size` must be at least 1 when provided.
- `total_man_month` must be zero or greater when provided.
- Technology names are trimmed, lowercased, and deduplicated.

Responses:

- `201 Created`: project created and returned as a `ProjectOut` object.
- `401 Unauthorized`: missing or invalid JWT.
- `422 Unprocessable Entity`: request validation failed.

## GET /projects/{project_id}

Return one active project by numeric id. The response includes the CSV-backed fields as arrays:

```json
{
  "id": 1,
  "customer_name": "ABC Corporation",
  "project_name": "Payment Platform",
  "start_date": "2026-04-01",
  "end_date": "2026-09-30",
  "is_ongoing": false,
  "technologies": ["python", "fastapi", "postgresql"],
  "project_types": ["new_dev"],
  "dev_process_phases": ["requirements", "design", "implementation", "testing"],
  "created_by": "user@example.com",
  "created_at": "2026-04-01T09:00:00",
  "updated_at": "2026-04-01T09:00:00"
}
```

Responses:

- `200 OK`: active project returned.
- `401 Unauthorized`: missing or invalid JWT.
- `404 Not Found`: id does not exist or the project was soft-deleted.

## Demo Flow

1. Register a user with `POST /auth/register`.
2. Login with `POST /auth/login` and save the returned `idToken`.
3. Send `POST /projects` with technologies, project types, and development phases.
4. Call `GET /projects` to confirm the created project and its arrays.
5. Call `GET /projects?q=Payment&technology=fastapi` to demonstrate search and filtering.
6. Call `GET /tech-tags?q=fast` to demonstrate autocomplete.
7. Call `PUT /projects/{project_id}` with the full replacement payload.
8. Call `DELETE /projects/{project_id}`, then verify `GET /projects/{project_id}` returns `404`.

## Project Structure

```text
app/
├── main.py
├── api/routers/       # auth, projects, and tech-tags routes
├── core/              # settings and JWT security
├── db/                # engine, session, and declarative base
├── models/            # User, Project, and TechTag
├── schemas/           # request and response validation models
├── services/          # project and user business logic
└── utils/             # CSV conversion and tag upsert helpers
alembic/               # database migrations
tests/                 # API tests
```

SQLite is the default development database. Run `alembic upgrade head` after setup and after pulling new migrations.