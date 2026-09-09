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

class ProjectUpdate(BaseModel):
    project_code: Optional[str] = None
    name: Optional[str] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None

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
