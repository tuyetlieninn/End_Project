from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import ColumnElement, false, func, literal, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectListOut, ProjectOut, ProjectUpdate
from app.utils.csv_helper import csv_to_list, list_to_csv
from app.utils.sql_like import LIKE_ESCAPE, escape_like
from app.utils.tag_upsert import upsert_tech_tags


def _csv_contains_any(
    column: InstrumentedAttribute[str], values: list[str]
) -> ColumnElement[bool] | None:
    # Match a whole item: look for ",java," in ",java,spring," (does not match "javascript")
    wanted = [value.strip().lower() for value in values if value.strip()]
    if not wanted:
        return None
    wrapped = func.lower(literal(",") + column + literal(","))
    conditions = [
        wrapped.like(f"%,{escape_like(value)},%", escape=LIKE_ESCAPE)
        for value in wanted
        if "," not in value  # a value containing "," can never be a single CSV item
    ]
    return or_(*conditions) if conditions else false()


def _to_out(project: Project) -> ProjectOut:
    return ProjectOut(
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
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


async def _get_active_project(db: AsyncSession, project_id: int) -> Project:
    # Shared by GET/PUT/DELETE: find a project that is not soft-deleted, otherwise 404
    stmt = select(Project).where(Project.id == project_id, Project.deleted_at.is_(None))
    result = await db.execute(stmt)
    project = result.scalars().first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


async def create_project(db: AsyncSession, payload: ProjectCreate, created_by: str) -> ProjectOut:
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
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return _to_out(project)


async def list_projects(
    db: AsyncSession,
    page: int,
    page_size: int,
    q: str | None,
    technology: list[str],
    project_type: list[str],
    dev_process_phase: list[str],
) -> ProjectListOut:
    stmt = select(Project).where(Project.deleted_at.is_(None))

    if q:
        # Escape LIKE wildcards so "%" and "_" are searched as literal characters
        pattern = f"%{escape_like(q)}%"
        stmt = stmt.where(
            or_(
                Project.customer_name.ilike(pattern, escape=LIKE_ESCAPE),
                Project.project_name.ilike(pattern, escape=LIKE_ESCAPE),
                Project.description.ilike(pattern, escape=LIKE_ESCAPE),
            )
        )

    # Multi-value filters: OR within one field; each value must match a whole CSV item
    for column, values in (
        (Project.technologies_csv, technology),
        (Project.project_types_csv, project_type),
        (Project.dev_process_phases_csv, dev_process_phase),
    ):
        condition = _csv_contains_any(column, values)
        if condition is not None:
            stmt = stmt.where(condition)

    # Count before paginating so "total" is the full result count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar_one()

    # Paginate last
    stmt = stmt.order_by(Project.id).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    projects = result.scalars().all()

    return ProjectListOut(
        items=[_to_out(p) for p in projects], total=total, page=page, page_size=page_size
    )


async def get_project(db: AsyncSession, project_id: int) -> ProjectOut:
    project = await _get_active_project(db, project_id)
    return _to_out(project)


async def update_project(db: AsyncSession, project_id: int, payload: ProjectUpdate) -> ProjectOut:
    project = await _get_active_project(db, project_id)
    await upsert_tech_tags(db, payload.technologies)

    # Full replacement: overwrite every field except created_by, which must not change
    project.customer_name = payload.customer_name
    project.project_name = payload.project_name
    project.description = payload.description
    project.start_date = payload.start_date
    project.end_date = payload.end_date
    project.is_ongoing = payload.is_ongoing
    project.team_size = payload.team_size
    project.total_man_month = payload.total_man_month
    project.source_note = payload.source_note
    project.industry = payload.industry
    project.outcome_note = payload.outcome_note
    project.team_composition_note = payload.team_composition_note
    project.technologies_csv = list_to_csv(payload.technologies)
    project.project_types_csv = list_to_csv([p.value for p in payload.project_types])
    project.dev_process_phases_csv = list_to_csv([p.value for p in payload.dev_process_phases])

    await db.commit()
    await db.refresh(project)
    return _to_out(project)


async def delete_project(db: AsyncSession, project_id: int) -> None:
    project = await _get_active_project(db, project_id)
    project.deleted_at = datetime.now(timezone.utc)  # soft delete: only set the column, keep the row
    await db.commit()