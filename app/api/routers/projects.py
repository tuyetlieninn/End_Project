from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead
from app.utils.csv_helper import csv_to_list, list_to_csv


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
) -> list[Project]:
    result = await db.execute(
        select(Project)
        .where(Project.owner_id == current_user.id)
        .order_by(Project.created_at.desc())
    )
    projects = list(result.scalars().all())
    for project in projects:
        project.technologies = csv_to_list(project.technologies_csv)
    return projects


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> Project:
    project = Project(
        name=payload.name,
        description=payload.description,
        status=payload.status,
        start_date=payload.start_date,
        end_date=payload.end_date,
        owner_id=current_user.id,
        technologies_csv=list_to_csv(payload.technologies),
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    project.technologies = csv_to_list(project.technologies_csv)
    return project