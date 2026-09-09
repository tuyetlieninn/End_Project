from fastapi import APIRouter
from app.api.auth_router import router as auth_router
from app.api.project_router import router as project_router
from app.api.tech_tag_router import router as tech_tag_router
from app.api.health_router import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(project_router)
api_router.include_router(tech_tag_router)
api_router.include_router(health_router)
