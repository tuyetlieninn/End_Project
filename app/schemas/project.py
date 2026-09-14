<<<<<<< HEAD
from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectBase(BaseModel):
    project_code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    customer_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

    project_type: str = Field(..., max_length=50)
    dev_process_phase: str = Field(..., max_length=50)

    status: str = Field(..., max_length=50)
    priority: int = 0

    leader_id: Optional[int] = None

    # CSV fields → convert to list in schema
    tech_stacks: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    urls: Optional[List[str]] = None
    members: Optional[List[str]] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    pass
=======
from enum import Enum

from pydantic import BaseModel, Field


class ProjectType(str, Enum):
    # Enum chính thức theo API仕様, KHÔNG được thêm giá trị ngoài danh sách này
    OFFSHORE = "offshore"
    SES = "ses"
    LAB = "lab"
    NEW_DEV = "new_dev"
    MAINTENANCE = "maintenance"


class DevProcessPhase(str, Enum):
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    RELEASE = "release"
    MAINTENANCE_OPS = "maintenance_ops"


class ProjectCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    project_name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_date: str  # dạng "YYYY-MM-DD"
    end_date: str | None = None
    is_ongoing: bool = False
    team_size: int | None = Field(default=None, ge=1)
    total_man_month: float | None = Field(default=None, ge=0)
    source_note: str | None = None
    industry: str | None = None
    outcome_note: str | None = None
    team_composition_note: str | None = None
    technologies: list[str] = []
    project_types: list[ProjectType] = []
    dev_process_phases: list[DevProcessPhase] = []
>>>>>>> develop

class ProjectUpdate(BaseModel):
    project_code: Optional[str] = None
    name: Optional[str] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None

<<<<<<< HEAD
    project_type: Optional[str] = None
    dev_process_phase: Optional[str] = None

    status: Optional[str] = None
    priority: Optional[int] = None

    leader_id: Optional[int] = None

    tech_stacks: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    urls: Optional[List[str]] = None
    members: Optional[List[str]] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
=======
# PUT là full replacement nên dùng chung schema với POST (không cho phép thiếu field như PATCH)
class ProjectUpdate(ProjectCreate):
    pass


class ProjectOut(BaseModel):
    id: int
    customer_name: str
    project_name: str
    description: str | None
    start_date: str
    end_date: str | None
    is_ongoing: bool
    team_size: int | None
    total_man_month: float | None
    source_note: str | None
    industry: str | None
    outcome_note: str | None
    team_composition_note: str | None
    technologies: list[str]
    project_types: list[str]
    dev_process_phases: list[str]
    created_by: str
    created_at: str
    updated_at: str


class ProjectListOut(BaseModel):
    items: list[ProjectOut]
    total: int
    page: int
    page_size: int
>>>>>>> develop
