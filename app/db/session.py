from sqlalchemy.orm import sessionmaker

from app.db.database import engine

# SessionLocal là factory tạo ra 1 phiên làm việc (session) với DB mỗi khi cần
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # Dependency dùng trong FastAPI: mở session, dùng xong tự đóng lại (kể cả khi lỗi)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()