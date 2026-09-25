from enum import Enum

from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class ProjectType(str, Enum):
    
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
    start_date: str
    end_date: str | None = None
    is_ongoing: bool = False
    team_size: int | None = Field(default=None, ge=1)
    total_man_month: float | None = Field(default=None, ge=0)
    source_note: str | None = None
    industry: str | None = None
    outcome_note: str | None = None
    team_composition_note: str | None = None
    technologies: list[str] = Field(default_factory=list)
    project_types: list[ProjectType] = Field(default_factory=list)
    dev_process_phases: list[DevProcessPhase] = Field(default_factory=list)

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("Date must use the YYYY-MM-DD format") from exc
        if len(value) != 10:
            raise ValueError("Date must use the YYYY-MM-DD format")
        return value

    @field_validator("technologies")
    @classmethod
    def normalize_technologies(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for value in values:
            tag = value.strip().lower()
            if tag and tag not in seen:
                normalized.append(tag)
                seen.add(tag)
        return normalized

    @model_validator(mode="after")
    def validate_period(self) -> "ProjectCreate":
        if self.is_ongoing and self.end_date is not None:
            raise ValueError("end_date must be omitted when is_ongoing is true")
        if self.end_date is not None and date.fromisoformat(self.end_date) < date.fromisoformat(
            self.start_date
        ):
            raise ValueError("end_date must be on or after start_date")
        return self


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
