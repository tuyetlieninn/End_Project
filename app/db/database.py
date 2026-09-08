from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Đường dẫn tới file SQLite, sẽ tạo file end_project.db trong thư mục gốc dự án
SQLALCHEMY_DATABASE_URL = "sqlite:///./end_project.db"

# check_same_thread=False cần thiết vì SQLite mặc định chỉ cho 1 thread dùng 1 connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Base là lớp cha mà tất cả các Model (User, Project, TechTag...) sẽ kế thừa
Base = declarative_base()