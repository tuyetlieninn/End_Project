<<<<<<< HEAD
from sqlalchemy import Column, Integer, String
from app.core.database import Base
=======
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
>>>>>>> develop


class TechTag(Base):
    __tablename__ = "tech_tags"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
=======
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
>>>>>>> develop
