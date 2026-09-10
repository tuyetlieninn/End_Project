from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_tag import TechTag


async def upsert_tech_tags(db: AsyncSession, names: list[str]) -> None:
    cleaned = list(dict.fromkeys(n.strip() for n in names if n.strip()))
    if not cleaned:
        return

    stmt = select(TechTag.name).where(TechTag.name.in_(cleaned))
    result = await db.execute(stmt)
    existing = set(result.scalars().all())

    new_tags = [TechTag(name=name) for name in cleaned if name not in existing]
    if new_tags:
        db.add_all(new_tags)
        await db.flush()