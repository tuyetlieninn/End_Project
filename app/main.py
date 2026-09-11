from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import auth, projects, tags
from app.db.database import Base, engine
from app.models import project, tech_tag, user  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(title="End_Project API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tags.router)


@app.get("/health")
def health():
    return {"status": "ok", "db": "sqlite"}