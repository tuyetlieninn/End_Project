<<<<<<< HEAD
from fastapi import APIRouter, Depends, Query, status
=======
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
<<<<<<< HEAD
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectListOut, ProjectOut, ProjectUpdate
from app.services import project_service
=======
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead
from app.utils.csv_helper import csv_to_list, list_to_csv

>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99

router = APIRouter(prefix="/projects", tags=["projects"])


<<<<<<< HEAD
@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # bắt buộc phải có JWT hợp lệ
) -> ProjectOut:
    # created_by LẤY TỪ current_user.email, KHÔNG lấy từ payload -> client không thể giả mạo
    return await project_service.create_project(db, payload, created_by=current_user.email)


@router.get("", response_model=ProjectListOut)
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    q: str | None = Query(default=None),
    technology: list[str] = Query(default=[]),
    project_type: list[str] = Query(default=[]),
    dev_process_phase: list[str] = Query(default=[]),
) -> ProjectListOut:
    return await project_service.list_projects(
        db, page, page_size, q, technology, project_type, dev_process_phase
    )


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectOut:
    return await project_service.get_project(db, project_id)


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectOut:
    return await project_service.update_project(db, project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    await project_service.delete_project(db, project_id)
=======
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
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
