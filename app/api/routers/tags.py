from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.tech_tag import TechTag
from app.schemas.tech_tag import TechTagCreate, TechTagRead


router = APIRouter(prefix="/tech-tags", tags=["tech-tags"])


@router.get("", response_model=list[str])
async def list_tags(
    q: str | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
) -> list[str]:
    statement = select(TechTag.name).order_by(TechTag.name)  # chỉ lấy cột name, không lấy cả object
    if q:
        statement = statement.where(TechTag.name.ilike(f"%{q}%"))
    result = await db.execute(statement.limit(20) if q else statement)
    return list(result.scalars().all())  # trả về list[str] thuần, không có id


@router.post("", response_model=TechTagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TechTagCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
) -> TechTag:
    tag = TechTag(name=payload.name.strip().lower())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag