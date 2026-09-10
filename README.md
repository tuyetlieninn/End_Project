# My Project Backend

Backend quan ly du an noi bo, xay dung voi FastAPI, SQLAlchemy async va Alembic.

## Chay nhanh

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Mo Swagger tai `http://127.0.0.1:8000/docs`.

## API chinh

- `POST /api/v1/auth/register`: tao tai khoan
- `POST /api/v1/auth/login`: dang nhap OAuth2 form, tra JWT
- `GET/POST /api/v1/projects`: xem va tao project cua user hien tai
- `GET/POST /api/v1/tags`: xem va tao tech tag
- `GET /health`: kiem tra service

SQLite duoc dung mac dinh de development. Doi `DATABASE_URL` trong `.env` khi ket noi PostgreSQL.

## Migration

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
