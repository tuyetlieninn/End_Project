from datetime import datetime
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.project import Project
from app.services.tech_tag_service import upsert_tech_tags, to_csv, from_csv
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project import ProjectType, DevProcessPhase


async def create_project_service(db: AsyncSession, data: ProjectCreate, user_id: int):
    # upsert technologies → list ID
    tech_ids = await upsert_tech_tags(db, data.technologies)

    project = Project(
        customer_name=data.customer_name,
        project_name=data.project_name,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        is_ongoing=data.is_ongoing,
        team_size=data.team_size,
        total_man_month=data.total_man_month,
        source_note=data.source_note,
        industry=data.industry,
        outcome_note=data.outcome_note,
        team_composition_note=data.team_composition_note,

        # CSV fields
        technologies_csv=to_csv([str(i) for i in tech_ids]),
        project_types_csv=to_csv([t.value for t in data.project_types]),
        dev_process_phases_csv=to_csv([p.value for p in data.dev_process_phases]),

        created_by=user_id,
        deleted_at=None,
        status="active",
        priority=0
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)

    # convert ID → name
    project.technologies = data.technologies
    return project


async def update_project_service(db: AsyncSession, project_id: int, data: ProjectUpdate):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project or project.deleted_at:
        raise HTTPException(404, "Project not found")

    update_data = data.model_dump(exclude_unset=True)

    # technologies
    if "technologies" in update_data:
        tech_ids = await upsert_tech_tags(db, update_data["technologies"])
        project.technologies_csv = to_csv([str(i) for i in tech_ids])
        update_data.pop("technologies")

    # project_types
    if "project_types" in update_data:
        project.project_types_csv = to_csv([t.value for t in update_data["project_types"]])
        update_data.pop("project_types")

    # dev_process_phases
    if "dev_process_phases" in update_data:
        project.dev_process_phases_csv = to_csv([p.value for p in update_data["dev_process_phases"]])
        update_data.pop("dev_process_phases")

    # update remaining fields
    for key, value in update_data.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)

    project.technologies = from_csv(project.technologies_csv)
    return project


async def get_project_service(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project or project.deleted_at:
        raise HTTPException(404, "Project not found")

    project.technologies = from_csv(project.technologies_csv)
    project.project_types = [ProjectType(v) for v in from_csv(project.project_types_csv)]
    project.dev_process_phases = [DevProcessPhase(v) for v in from_csv(project.dev_process_phases_csv)]

    return project


async def soft_delete_project_service(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project or project.deleted_at:
        raise HTTPException(404, "Project not found")

    project.deleted_at = datetime.utcnow()
    await db.commit()
    return True


async def list_projects_service(
    db: AsyncSession,
    page: int,
    page_size: int,
    q: str | None,
    project_types: list[str] | None,
    dev_process_phases: list[str] | None,
    technologies: list[str] | None
):
    stmt = select(Project).where(Project.deleted_at.is_(None))

    # full-text search
    if q:
        stmt = stmt.where(
            or_(
                Project.project_name.ilike(f"%{q}%"),
                Project.description.ilike(f"%{q}%")
            )
        )

    # filter project_types
    if project_types:
        for pt in project_types:
            stmt = stmt.where(Project.project_types_csv.ilike(f"%{pt}%"))

    # filter dev_process_phases
    if dev_process_phases:
        for dp in dev_process_phases:
            stmt = stmt.where(Project.dev_process_phases_csv.ilike(f"%{dp}%"))

    # filter technologies (by ID)
    if technologies:
        for tech in technologies:
            stmt = stmt.where(Project.technologies_csv.ilike(f"%{tech}%"))

    # pagination
    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(total_stmt)).scalar()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    projects = result.scalars().all()

    # convert CSV → array
    for p in projects:
        p.technologies = from_csv(p.technologies_csv)
        p.project_types = from_csv(p.project_types_csv)
        p.dev_process_phases = from_csv(p.dev_process_phases_csv)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": projects
    }
