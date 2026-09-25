from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
    normalized_name = payload.name.strip().lower()
    existing_tag = await db.scalar(select(TechTag).where(TechTag.name == normalized_name))
    if existing_tag is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")

    tag = TechTag(name=normalized_name)
    db.add(tag)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag already exists")
    await db.refresh(tag)
    return tag