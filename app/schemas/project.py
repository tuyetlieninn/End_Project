from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class ProjectType(str, Enum):
    offshore = "offshore"
    ses = "ses"
    lab = "lab"
    new_dev = "new_dev"
    maintenance = "maintenance"


class DevProcessPhase(str, Enum):
    requirements = "requirements"
    design = "design"
    implementation = "implementation"
    testing = "testing"
    release = "release"
    maintenance_ops = "maintenance_ops"


class ProjectBase(BaseModel):
    customer_name: str
    project_name: str
    description: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: bool = False

    team_size: int
    total_man_month: int

    source_note: Optional[str] = None
    industry: Optional[str] = None
    outcome_note: Optional[str] = None
    team_composition_note: Optional[str] = None

    technologies: List[str] = []
    project_types: List[ProjectType] = []
    dev_process_phases: List[DevProcessPhase] = []


class ProjectCreate(ProjectBase):
    status: str = "active"
    priority: int = 0


class ProjectUpdate(BaseModel):
    customer_name: Optional[str] = None
    project_name: Optional[str] = None
    description: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: Optional[bool] = None

    team_size: Optional[int] = None
    total_man_month: Optional[int] = None

    source_note: Optional[str] = None
    industry: Optional[str] = None
    outcome_note: Optional[str] = None
    team_composition_note: Optional[str] = None

    technologies: Optional[List[str]] = None
    project_types: Optional[List[ProjectType]] = None
    dev_process_phases: Optional[List[DevProcessPhase]] = None

    status: Optional[str] = None
    priority: Optional[int] = None


class ProjectRead(ProjectBase):
    id: int
    created_by: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    status: str
    priority: int

    leader_id: Optional[int] = None
    tech_stacks: Optional[str] = None
    tags: Optional[str] = None
    urls: Optional[str] = None
    members: Optional[str] = None

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[ProjectRead]
