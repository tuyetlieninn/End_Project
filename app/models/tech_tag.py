from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TechTag(Base):
    __tablename__ = "tech_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<TechTag id={self.id} name={self.name}>"
