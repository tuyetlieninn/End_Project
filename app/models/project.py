<<<<<<< HEAD
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime
)
from sqlalchemy.orm import declarative_base
from datetime import datetime
=======
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
>>>>>>> develop

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)

    project_code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    customer_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    project_type = Column(String(50), nullable=False)
    dev_process_phase = Column(String(50), nullable=False)

    status = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False, default=0)

    leader_id = Column(Integer, nullable=True)

  
    tech_stacks = Column(Text, nullable=True)   # JSON s
    tags = Column(Text, nullable=True)
    urls = Column(Text, nullable=True)
    members = Column(Text, nullable=True)

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    deleted_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
=======
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[str] = mapped_column(String(10), nullable=False)
    end_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    team_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_man_month: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    outcome_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    team_composition_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    technologies_csv: Mapped[str] = mapped_column(String(2000), nullable=False, default="")
    project_types_csv: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    dev_process_phases_csv: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
>>>>>>> develop
