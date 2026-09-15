from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tech_tag import TechTag

async def upsert_tech_tags(db: AsyncSession, technologies: list[str]) -> list[int]:
    tag_ids = []

    for tech in technologies:
        tech = tech.strip().lower()

        stmt = select(TechTag).where(TechTag.name == tech)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            tag_ids.append(existing.id)
        else:
            new_tag = TechTag(name=tech)
            db.add(new_tag)
            await db.flush()  # lấy id ngay
            tag_ids.append(new_tag.id)

    return tag_ids
