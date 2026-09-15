from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_tag import TechTag


async def get_or_create_tag(db: AsyncSession, name: str) -> TechTag:
    # chuẩn hóa dữ liệu
    normalized_name = name.strip().lower()

    if not normalized_name:
        return None  # hoặc raise HTTPException(400, "Invalid technology name")

    # kiểm tra tồn tại
    result = await db.execute(
        select(TechTag).where(TechTag.name == normalized_name)
    )
    tag = result.scalar_one_or_none()

    if tag:
        return tag

    # tạo mới
    tag = TechTag(name=normalized_name)
    db.add(tag)
    await db.flush()  # để lấy id ngay
    return tag
