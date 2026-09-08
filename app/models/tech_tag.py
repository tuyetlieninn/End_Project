from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TechTag(Base):
    __tablename__ = "tech_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)

    projects: Mapped[list["Project"]] = relationship(
        secondary="project_tags", back_populates="tags"
    )
