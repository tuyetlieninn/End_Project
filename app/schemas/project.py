from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectTypes(StrEnum):
    OFFSHORE = "offshore"
    SES = "ses"
    LAB = "lab"
    NEW_DEV = "new_dev"
    MAINTENANCE = "maintenance"


class DevProcessPhases(StrEnum):
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    RELEASE = "release"
    MAINTENANCE_OPS = "maintenance_ops"


def validate_iso_date(value: str | None) -> str | None:
    if value is not None:
        date.fromisoformat(value)
    return value


class ProjectCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=255)
    project_name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    is_ongoing: bool = False
    team_size: int | None = Field(default=None, ge=1)
    total_man_month: float | None = Field(default=None, ge=0)
    source_note: str | None = None
    industry: str | None = None
    outcome_note: str | None = None
    team_composition_note: str | None = None
    technologies: list[str] = Field(default_factory=list)
    project_types: list[ProjectTypes] = Field(default_factory=list)
    dev_process_phases: list[DevProcessPhases] = Field(default_factory=list)

    _validate_start_date = field_validator("start_date")(validate_iso_date)
    _validate_end_date = field_validator("end_date")(validate_iso_date)


class ProjectUpdate(ProjectCreate):
    pass


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    technologies: list[str] = Field(default_factory=list)
    project_types: list[ProjectTypes] = Field(default_factory=list)
    dev_process_phases: list[DevProcessPhases] = Field(default_factory=list)
    created_by: str
    created_at: datetime
    updated_at: datetime


ProjectRead = ProjectOut

ProjectType = ProjectTypes
DevProcessPhase = DevProcessPhases
