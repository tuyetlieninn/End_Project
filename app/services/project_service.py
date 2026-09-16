from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectListResponse, ProjectRead, ProjectUpdate
from app.utils.csv_helper import csv_to_list, list_to_csv
from app.utils.tag_upsert import upsert_tech_tags


def _to_read(project: Project) -> ProjectRead:
    return ProjectRead(
        id=project.id,
        customer_name=project.customer_name,
        project_name=project.project_name,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        is_ongoing=project.is_ongoing,
        team_size=project.team_size,
        total_man_month=project.total_man_month,
        source_note=project.source_note,
        industry=project.industry,
        outcome_note=project.outcome_note,
        team_composition_note=project.team_composition_note,
        technologies=csv_to_list(project.technologies_csv),
        project_types=csv_to_list(project.project_types_csv),
        dev_process_phases=csv_to_list(project.dev_process_phases_csv),
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
        deleted_at=project.deleted_at,
        status=project.status,
        priority=project.priority,
        leader_id=project.leader_id,
        tech_stacks=project.tech_stacks,
        tags=project.tags,
        urls=project.urls,
        members=project.members,
    )


async def _get_active_project(db: AsyncSession, project_id: int) -> Project:
    stmt = select(Project).where(Project.id == project_id, Project.deleted_at.is_(None))
    result = await db.execute(stmt)
    project = result.scalars().first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def create_project_service(db: AsyncSession, payload: ProjectCreate, created_by: int):
    await upsert_tech_tags(db, payload.technologies)

    project = Project(
        customer_name=payload.customer_name,
        project_name=payload.project_name,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_ongoing=payload.is_ongoing,
        team_size=payload.team_size,
        total_man_month=payload.total_man_month,
        source_note=payload.source_note,
        industry=payload.industry,
        outcome_note=payload.outcome_note,
        team_composition_note=payload.team_composition_note,
        technologies_csv=list_to_csv(payload.technologies),
        project_types_csv=list_to_csv([p.value for p in payload.project_types]),
        dev_process_phases_csv=list_to_csv([p.value for p in payload.dev_process_phases]),
        created_by=created_by,
        status=payload.status,
        priority=payload.priority,
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _to_read(project)


async def list_projects_service(
    db: AsyncSession,
    page: int,
    page_size: int,
    q: str | None,
    technologies: list[str],
    project_types: list[str],
    dev_process_phases: list[str],
):
    stmt = select(Project).where(Project.deleted_at.is_(None))

    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Project.customer_name.ilike(pattern),
                Project.project_name.ilike(pattern),
                Project.description.ilike(pattern),
            )
        )

    if technologies:
        stmt = stmt.where(or_(*[Project.technologies_csv.contains(t) for t in technologies]))

    if project_types:
        stmt = stmt.where(or_(*[Project.project_types_csv.contains(t) for t in project_types]))

    if dev_process_phases:
        stmt = stmt.where(or_(*[Project.dev_process_phases_csv.contains(p) for p in dev_process_phases]))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    stmt = stmt.order_by(Project.id).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    projects = result.scalars().all()

    return ProjectListResponse(
        page=page,
        page_size=page_size,
        total=total,
        items=[_to_read(p) for p in projects],
    )


async def get_project_service(db: AsyncSession, project_id: int):
    project = await _get_active_project(db, project_id)
    return _to_read(project)


async def update_project_service(db: AsyncSession, project_id: int, payload: ProjectUpdate):
    project = await _get_active_project(db, project_id)

    update_data = payload.model_dump(exclude_unset=True)

    if "technologies" in update_data:
        await upsert_tech_tags(db, update_data["technologies"])
        project.technologies_csv = list_to_csv(update_data["technologies"])
        update_data.pop("technologies")

    if "project_types" in update_data:
        project.project_types_csv = list_to_csv([p.value for p in update_data["project_types"]])
        update_data.pop("project_types")

    if "dev_process_phases" in update_data:
        project.dev_process_phases_csv = list_to_csv([p.value for p in update_data["dev_process_phases"]])
        update_data.pop("dev_process_phases")

    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return _to_read(project)


async def soft_delete_project_service(db: AsyncSession, project_id: int):
    project = await _get_active_project(db, project_id)
    project.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    return True

