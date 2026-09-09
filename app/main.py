from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.api import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import project, tech_tag, user

import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router, prefix=settings.api_v1_prefix)