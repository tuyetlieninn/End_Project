from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_tag import TechTag


<<<<<<< HEAD
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
=======
def _normalize_tag_name(name: str) -> str:
    return name.strip().lower()


async def get_or_create_tag(db: AsyncSession, name: str) -> TechTag:
    normalized_name = _normalize_tag_name(name)
    result = await db.execute(select(TechTag).where(TechTag.name == normalized_name))
    tag = result.scalar_one_or_none()
    if tag:
        return tag

    tag = TechTag(name=normalized_name)
    db.add(tag)
    await db.flush()
    return tag


async def upsert_tech_tags(db: AsyncSession, names: list[str]) -> list[TechTag]:
    normalized_names = list(dict.fromkeys(_normalize_tag_name(name) for name in names))
    normalized_names = [name for name in normalized_names if name]
    if not normalized_names:
        return []

    result = await db.execute(
        select(TechTag).where(TechTag.name.in_(normalized_names))
    )
    existing_tags = {tag.name: tag for tag in result.scalars().all()}

    for name in normalized_names:
        if name not in existing_tags:
            tag = TechTag(name=name)
            db.add(tag)
            existing_tags[name] = tag

    await db.flush()
    return [existing_tags[name] for name in normalized_names]
>>>>>>> 49ffcc3b96e5f92295b46119e01730961230be99
