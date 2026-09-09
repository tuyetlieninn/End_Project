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

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

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
