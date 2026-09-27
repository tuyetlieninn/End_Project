from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routers import auth, projects, tags
from app.db.session import get_db
from app.models.project import Project
from app.models.tech_tag import TechTag
from app.models.user import User


app = FastAPI(title="End_Project API")


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
async def health(db: AsyncSession = Depends(get_db)):
    # Query every table so a database that has not been migrated
    # (`alembic upgrade head`) is reported as not ready instead of "ok".
    try:
        for model in (User, Project, TechTag):
            await db.execute(select(model.id).limit(1))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "error", "db": "error"},
        )
    return {"status": "ok", "db": "ok"}