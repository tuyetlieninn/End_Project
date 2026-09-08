from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.models.project import Project
from app.models.tech_tag import TechTag
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead])
async def list_projects(db: DbSession, current_user: CurrentUser) -> list[Project]:
    result = await db.execute(
        select(Project)
        .where(Project.owner_id == current_user.id)
        .options(selectinload(Project.tags))
        .order_by(Project.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate, db: DbSession, current_user: CurrentUser
) -> Project:
    tags = list(
        (await db.execute(select(TechTag).where(TechTag.id.in_(payload.tag_ids))))
        .scalars()
        .all()
    )
    if len(tags) != len(set(payload.tag_ids)):
        raise HTTPException(status_code=400, detail="One or more tag IDs do not exist")

    project = Project(
        name=payload.name,
        description=payload.description,
        status=payload.status,
        start_date=payload.start_date,
        end_date=payload.end_date,
        owner_id=current_user.id,
        tags=tags,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project, ["tags"])
    return project
