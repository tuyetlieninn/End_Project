from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

<<<<<<< HEAD
from app.api.api import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import project, tech_tag, user

import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
=======
from app.api.routers import auth, projects, tags
from app.db.database import Base, engine
from app.models import project, tech_tag, user  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
>>>>>>> develop
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


<<<<<<< HEAD
app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router, prefix=settings.api_v1_prefix)
=======
app = FastAPI(title="End_Project API", lifespan=lifespan)

# Cho phép frontend (chạy ở port 5173) gọi được API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tags.router)


@app.get("/health")
def health():
    return {"status": "ok", "db": "ok"}
>>>>>>> develop
