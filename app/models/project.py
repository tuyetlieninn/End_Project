from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    # --- SPEC FIELDS (INTERN2026-61) ---
    customer_name = Column(String(255), nullable=False)
    project_name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    start_date = Column(String(10), nullable=False)      # YYYY-MM-DD
    end_date = Column(String(10), nullable=False)

    is_ongoing = Column(Boolean, nullable=False, default=False)
    team_size = Column(Integer, nullable=False)          # >= 1
    total_man_month = Column(Integer, nullable=False)    # >= 0

    source_note = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    outcome_note = Column(String, nullable=True)
    team_composition_note = Column(String, nullable=True)

    # CSV fields (task 61)
    technologies_csv = Column(String, nullable=True)
    project_types_csv = Column(String, nullable=True)
    dev_process_phases_csv = Column(String, nullable=True)

    created_by = Column(Integer, nullable=False)

    # --- TIMESTAMPS ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # --- EXTRA FIELDS FROM TASK 63 ---
    status = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)

    leader_id = Column(Integer, nullable=True)
    tech_stacks = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    urls = Column(String, nullable=True)
    members = Column(String, nullable=True)
