from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectRead, ProjectListResponse
from app.services.project_service import (
    create_project_service,
    update_project_service,
    get_project_service,
    list_projects_service,
    soft_delete_project_service
)
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=ProjectListResponse)
async def list_projects_api(
    page: int = 1,
    page_size: int = 10,
    q: str | None = None,
    project_types: list[str] | None = None,
    dev_process_phases: list[str] | None = None,
    technologies: list[str] | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await list_projects_service(
        db=db,
        page=page,
        page_size=page_size,
        q=q,
        project_types=project_types,
        dev_process_phases=dev_process_phases,
        technologies=technologies
    )


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project_api(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_project_service(db, data, current_user.id)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project_api(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_project_service(db, project_id)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project_api(
    project_id: int,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_project_service(db, project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_api(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await soft_delete_project_service(db, project_id)
    return
