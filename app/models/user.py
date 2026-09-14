<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
=======
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
>>>>>>> develop

class User(Base):
    __tablename__ = "users"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="member")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
=======
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # đổi tên từ hashed_password thành password_hash cho đúng data model
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="member")
    # cột mới, tự động lấy giờ hiện tại (UTC) lúc tạo record
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
>>>>>>> develop
