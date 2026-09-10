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
