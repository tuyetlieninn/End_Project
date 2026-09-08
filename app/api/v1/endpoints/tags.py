from fastapi import APIRouter, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.models.tech_tag import TechTag
from app.schemas.tech_tag import TechTagCreate, TechTagRead

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TechTagRead])
async def list_tags(db: DbSession, _: CurrentUser) -> list[TechTag]:
    result = await db.execute(select(TechTag).order_by(TechTag.name))
    return list(result.scalars().all())


@router.post("", response_model=TechTagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(payload: TechTagCreate, db: DbSession, _: CurrentUser) -> TechTag:
    tag = TechTag(name=payload.name.strip().lower())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag
