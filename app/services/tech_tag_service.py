from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tech_tag import TechTag


async def get_or_create_tag(db: AsyncSession, name: str) -> TechTag:
    normalized = name.strip().lower()
    if not normalized:
        return None

    result = await db.execute(
        select(TechTag).where(TechTag.name == normalized)
    )
    tag = result.scalar_one_or_none()
    if tag:
        return tag

    tag = TechTag(name=normalized)
    db.add(tag)
    await db.flush()
    return tag


async def upsert_tech_tags(db: AsyncSession, technologies: list[str]) -> list[int]:
    """Trả về list ID của tech_tags để lưu CSV vào DB."""
    if not technologies:
        return []

    tag_ids = []
    seen = set()

    for tech in technologies:
        normalized = tech.strip().lower()
        if not normalized or normalized in seen:
            continue

        seen.add(normalized)

        tag = await get_or_create_tag(db, normalized)
        tag_ids.append(tag.id)

    return tag_ids


def to_csv(values: list[str]) -> str:
    return ",".join(values)

def from_csv(csv_str: str) -> list[str]:
    if not csv_str:
        return []
    return [item.strip() for item in csv_str.split(",") if item.strip()]
