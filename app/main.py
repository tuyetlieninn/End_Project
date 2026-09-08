from fastapi import FastAPI

from app.api.routers import auth
from app.db.database import Base, engine
from app.models import user  # noqa: F401  (import để SQLAlchemy biết bảng users tồn tại)

# Tự tạo bảng trong SQLite nếu chưa có (dùng tạm, sau này Người A sẽ thay bằng Alembic migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="End_Project API")

app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok", "db": "sqlite"}