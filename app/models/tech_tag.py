from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TechTag(Base):
    __tablename__ = "tech_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
<<<<<<< HEAD
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
=======
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
