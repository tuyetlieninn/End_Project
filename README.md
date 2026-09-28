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

The API no longer creates tables on startup, so every request fails with a 500 error until the migrations have been applied.

If you already have a local database that was created by an older version of the app (tables created on startup, no `alembic_version` table), `alembic upgrade head` stops with `table tech_tags already exists`. Either delete that database file and run `alembic upgrade head` again (local data is lost), or, if its tables already match the current models, mark it as up to date without re-creating anything:

```bash
alembic stamp head
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
| GET | `/tech-tags?q=<text>` | Return technology tag names (up to 20 when `q` is given). |
| POST | `/tech-tags` | Create a normalized technology tag. Duplicate names return `409`. |

There are no legacy project routers or duplicate model implementations. The active API is registered from `app/api/routers/auth.py`, `projects.py`, and `tags.py`.

## GET /projects

List active (not soft-deleted) projects, ordered by `id` ascending, with keyword search, filters, and pagination.

Query parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `page` | integer ≥ 1 | `1` | Page number. A page past the last one returns an empty `items` list with the real `total`. |
| `page_size` | integer 1–100 | `20` | Projects per page. |
| `q` | string | – | Keyword. Partial, case-insensitive match on `customer_name`, `project_name`, `description`, and `technologies`. `%`, `_`, and `\` are matched as literal characters. |
| `technology` | string, repeatable | – | Technology tag, for example `technology=python&technology=go`. |
| `project_type` | string, repeatable | – | `offshore`, `ses`, `lab`, `new_dev`, `maintenance`. |
| `dev_process_phase` | string, repeatable | – | `requirements`, `design`, `implementation`, `testing`, `release`, `maintenance_ops`. |

Filter rules:

- Values of the same filter are combined with **OR**: `technology=python&technology=go` returns projects using python or go.
- Different filters and the keyword are combined with **AND**: `q=Bank&technology=java&project_type=lab`.
- Filter values match a **whole** item, case-insensitively: `technology=java` does not return projects that only use `javascript`, and `dev_process_phase=maintenance` does not match `maintenance_ops`.
- Empty filter values are ignored. An unknown value (for example `project_type=abc`) returns no projects.

Example:

```text
GET /projects?q=payment&technology=fastapi&project_type=lab&page=1&page_size=20
```

```json
{
  "items": [
    {
      "id": 1,
      "customer_name": "Fintech Co",
      "project_name": "Payment App",
      "description": "Payment processing system",
      "start_date": "2026-01-01",
      "end_date": null,
      "is_ongoing": true,
      "team_size": 5,
      "total_man_month": 12.5,
      "source_note": null,
      "industry": "Finance",
      "outcome_note": null,
      "team_composition_note": null,
      "technologies": ["python", "fastapi"],
      "project_types": ["lab"],
      "dev_process_phases": ["design", "implementation"],
      "created_by": "user@example.com",
      "created_at": "2026-01-01T09:00:00",
      "updated_at": "2026-01-01T09:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

`total` is the number of matching projects across all pages, so the number of pages is `ceil(total / page_size)`.

Responses:

- `200 OK`: page of projects returned (possibly empty).
- `401 Unauthorized`: missing, invalid, or expired JWT.
- `422 Unprocessable Entity`: `page` < 1, `page_size` outside 1–100, or a non-integer value.

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

- `customer_name`, `project_name`, and `start_date` are required. Names are trimmed and must not be blank.
- Dates must be real dates in `YYYY-MM-DD` format.
- `end_date` must be on or after `start_date`.
- `end_date` must be omitted when `is_ongoing` is `true`.
- `team_size` must be at least 1 when provided.
- `total_man_month` must be zero or greater when provided.
- Technology names are trimmed, lowercased, and deduplicated. They must not contain a comma and must be at most 100 characters.

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

## GET /tech-tags

Technology tag names for the autocomplete in the project form and the 技術 filter on the project list. Tags are created automatically when a project uses a new technology, and are always stored lowercase.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `q` | string | – | Partial, case-insensitive match on the tag name. `%`, `_`, and `\` are matched as literal characters. |

- Without `q`: every tag, sorted by name.
- With `q`: at most 20 matching tags, sorted by name.

Example:

```text
GET /tech-tags?q=py
```

```json
["python"]
```

Responses:

- `200 OK`: JSON array of tag names (an empty array when nothing matches).
- `401 Unauthorized`: missing, invalid, or expired JWT.

## Demo Data

With the API running, these scripts create data through the API (run them from the repository root). They log in with `--email` / `--password`, or the `SEED_EMAIL` / `SEED_PASSWORD` environment variables; without them they use the demo account `demo@example.com` / `Demo12345`, registering it if needed.

| Script | What it does |
| --- | --- |
| `python scripts/seed_demo_data.py` | Fixed data for the Project List demo and test cases: 45 projects `Project 001`–`Project 045` plus 8 sample projects (52 visible, 3 pages). Safe to run again, no duplicates. |
| `python scripts/generate_projects.py --count 50` | Creates random projects. |
| `python scripts/update_all_projects.py` | Overwrites **every** existing project with random data (asks for confirmation; `--yes` skips it). |

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
scripts/               # demo and random data generators
tests/                 # API tests
```

SQLite is the default development database. Run `alembic upgrade head` after setup and after pulling new migrations.