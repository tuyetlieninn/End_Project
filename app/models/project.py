from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    start_date: Mapped[str] = mapped_column(String(10), nullable=False)
    end_date: Mapped[str | None] = mapped_column(String(10))
    is_ongoing: Mapped[bool] = mapped_column(nullable=False, default=False)
    team_size: Mapped[int | None] = mapped_column(Integer)
    total_man_month: Mapped[float | None] = mapped_column()
    source_note: Mapped[str | None] = mapped_column(Text())
    industry: Mapped[str | None] = mapped_column(String(255))
    outcome_note: Mapped[str | None] = mapped_column(Text())
    team_composition_note: Mapped[str | None] = mapped_column(Text())
    technologies_csv: Mapped[str] = mapped_column(
        String(2000), nullable=False, default=""
    )
    project_types_csv: Mapped[str] = mapped_column(
        String(500), nullable=False, default=""
    )
    dev_process_phases_csv: Mapped[str] = mapped_column(
        String(500), nullable=False, default=""
    )
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
