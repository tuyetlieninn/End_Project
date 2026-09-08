from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Table, Column, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


project_tags = Table(
    "project_tags",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tech_tags.id", ondelete="CASCADE"), primary_key=True),
)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    status: Mapped[str] = mapped_column(String(40), default="planned")
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped["User"] = relationship(back_populates="projects")
    tags: Mapped[list["TechTag"]] = relationship(
        secondary=project_tags, back_populates="projects"
    )
