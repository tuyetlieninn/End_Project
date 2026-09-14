

Readme · MD
End_Project Backend
Internal project performance management backend (実績管理システム), built with FastAPI, async SQLAlchemy, and SQLite.

Quick Start
bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Create a .env file in the project root:

SECRET_KEY=your-secret-key-here
Run the server:

bash
uvicorn app.main:app --reload
Open the Swagger UI at http://127.0.0.1:8000/docs.

Run Tests
bash
python -m pytest tests/ -v
API Endpoints
Method	Path	Auth	Description
POST	/auth/register	No	Register a new account (role defaults to member)
POST	/auth/login	No	Log in and receive idToken
GET	/projects	Yes	List projects (pagination, search q, filters)
POST	/projects	Yes	Create a project (created_by is taken from the JWT, not the request body)
GET	/projects/{id}	Yes	Get project detail (404 if not found or soft-deleted)
PUT	/projects/{id}	Yes	Full replace update (404 if not found or soft-deleted)
DELETE	/projects/{id}	Yes	Soft delete (deleted_at), no physical delete
GET	/tech-tags?q=	Yes	Autocomplete technology tags (case-insensitive, max 20 results)
All endpoints except /auth/* and /health require a valid JWT in the Authorization: Bearer <idToken> header.

Demo Flow
POST /auth/register → get idToken
POST /projects with technologies, project_types, dev_process_phases arrays
GET /projects?q=...&technology=...&page=1&page_size=20
GET /tech-tags?q=py
PUT /projects/{id} to update, DELETE /projects/{id} to soft-delete
Project Structure
app/
├── main.py
├── core/          # config, security (JWT, password hashing)
├── db/            # database engine, session
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # business logic
├── api/routers/   # FastAPI routes
└── utils/         # CSV helper, tech tag upsert
tests/             # pytest tests
SQLite is used by default (end_project.db, created automatically on startup).


