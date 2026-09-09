from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.csv_helper import list_to_csv, csv_to_list
from datetime import datetime


def get_projects(db: Session):
    return db.query(Project).filter(Project.deleted_at.is_(None)).all()


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id, Project.deleted_at.is_(None)).first()


def create_project(db: Session, data: ProjectCreate):
    project = Project(
        project_code=data.project_code,
        name=data.name,
        customer_name=data.customer_name,
        description=data.description,
        project_type=data.project_type,
        dev_process_phase=data.dev_process_phase,
        status=data.status,
        priority=data.priority,
        leader_id=data.leader_id,
        tech_stacks_csv=list_to_csv(data.tech_stacks),
        tags_csv=list_to_csv(data.tags),
        urls_csv=list_to_csv(data.urls),
        members_csv=list_to_csv(data.members),
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: int, data: ProjectUpdate):
    project = get_project(db, project_id)
    if not project:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        if field in ["tech_stacks", "tags", "urls", "members"]:
            setattr(project, f"{field}_csv", list_to_csv(value))
        else:
            setattr(project, field, value)

    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int):
    project = get_project(db, project_id)
    if not project:
        return None

    project.deleted_at = datetime.utcnow()
    db.commit()
    return project
