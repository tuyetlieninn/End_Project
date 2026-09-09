from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.tech_tag import TechTag
from app.schemas.tech_tag import TechTagCreate, TechTagRead
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/tech-tags", tags=["tech-tags"])


@router.get("/", response_model=list[TechTagRead])
async def list_tags(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(TechTag))
    return result.scalars().all()


@router.post("/", response_model=TechTagRead)
async def create_tag(
    data: TechTagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tag = TechTag(**data.dict())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@router.get("/{tag_id}", response_model=TechTagRead)
async def get_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(TechTag).where(TechTag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(404, "Tech tag not found")
    return tag


@router.put("/{tag_id}", response_model=TechTagRead)
async def update_tag(
    tag_id: int,
    data: TechTagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(TechTag).where(TechTag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(404, "Tech tag not found")

    for key, value in data.dict().items():
        setattr(tag, key, value)

    await db.commit()
    await db.refresh(tag)
    return tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(TechTag).where(TechTag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(404, "Tech tag not found")

    await db.delete(tag)
    await db.commit()
    return {"message": "Tech tag deleted"}
