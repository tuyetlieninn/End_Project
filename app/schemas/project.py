<<<<<<< HEAD
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
=======
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: str = Field(default="planned", max_length=40)
    start_date: date | None = None
    end_date: date | None = None
    technologies: list[str] = Field(default_factory=list)


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    status: str
    start_date: date | None
    end_date: date | None
    owner_id: int
    created_at: datetime
    technologies: list[str] = Field(default_factory=list)
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
