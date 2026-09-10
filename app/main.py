from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import auth, projects
from app.db.database import Base, engine
from app.models import project, user  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chạy lúc server khởi động — engine.begin() mở 1 connection async
    # conn.run_sync(...) cho phép chạy hàm sync (create_all) bên trong context async
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # (nếu cần dọn dẹp lúc tắt server thì viết sau chữ yield, hiện chưa cần)


app = FastAPI(title="End_Project API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)


@app.get("/health")
def health():
    return {"status": "ok", "db": "sqlite"}