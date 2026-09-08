from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_tag import TechTag


async def get_or_create_tag(db: AsyncSession, name: str) -> TechTag:
    normalized_name = name.strip().lower()
    result = await db.execute(select(TechTag).where(TechTag.name == normalized_name))
    tag = result.scalar_one_or_none()
    if tag:
        return tag

    tag = TechTag(name=normalized_name)
    db.add(tag)
    await db.flush()
    return tag
