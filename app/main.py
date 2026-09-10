from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import auth, projects, tags
from app.db.database import Base, engine
from app.models import project, tech_tag, user  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="End_Project API", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tags.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
