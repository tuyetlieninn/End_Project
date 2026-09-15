from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.crud.tech_tag_crud import upsert_tech_tags


async def get_projects(db: AsyncSession) -> list[Project]:
    stmt = select(Project).where(Project.deleted_at.is_(None))
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    stmt = select(Project).where(
        Project.id == project_id,
        Project.deleted_at.is_(None)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


def _validate_dates(start_date, end_date):
    if start_date and end_date and start_date > end_date:
        raise ValueError("start_date must be before or equal to end_date")


async def create_project(db: AsyncSession, data: ProjectCreate) -> Project:
    _validate_dates(data.start_date, data.end_date)

    # chuẩn hóa technologies
    technologies = list({t.strip().lower() for t in data.technologies})

    # upsert tech_tags
    tag_ids = await upsert_tech_tags(db, technologies)

    # bỏ trường technologies khỏi model_dump để tránh conflict
    base_data = data.model_dump(exclude={"technologies"})

    project = Project(
        **base_data,
        technologies_csv=",".join(technologies),
        tech_tag_ids=",".join(map(str, tag_ids))
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project(
    db: AsyncSession,
    project_id: int,
    data: ProjectUpdate
) -> Project | None:
    project = await get_project(db, project_id)
    if not project:
        return None

    update_data = data.model_dump(exclude_unset=True)

    start = update_data.get("start_date", project.start_date)
    end = update_data.get("end_date", project.end_date)
    _validate_dates(start, end)

    # xử lý technologies riêng
    technologies = update_data.pop("technologies", None)
    if technologies is not None:
        normalized = list({t.strip().lower() for t in technologies})
        tag_ids = await upsert_tech_tags(db, normalized)

        project.technologies_csv = ",".join(normalized)
        project.tech_tag_ids = ",".join(map(str, tag_ids))

    # update các field còn lại
    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    project = await get_project(db, project_id)
    if not project:
        return False

    project.deleted_at = datetime.utcnow()
    await db.commit()
    return True


async def search_project(
    db: AsyncSession,
    status: str | None,
    leader_id: int | None,
    project_type: str | None,
    tag: str | None
):
    query = select(Project).where(Project.deleted_at.is_(None))

    if status:
        query = query.where(Project.status == status)

    if leader_id:
        query = query.where(Project.leader_id == leader_id)

    if project_type:
        query = query.where(Project.project_type == project_type)

    # search theo technologies_csv (text tag)
    if tag:
        query = query.where(Project.technologies_csv.like(f"%{tag}%"))

    result = await db.execute(query)
    return result.scalars().all()
