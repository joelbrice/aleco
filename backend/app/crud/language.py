"""CRUD operations for Language."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.language import Language
from app.schemas.language import LanguageCreate, LanguageUpdate


async def get_language(db: AsyncSession, language_id: int) -> Optional[Language]:
    result = await db.execute(select(Language).where(Language.id == language_id))
    return result.scalar_one_or_none()


async def get_language_by_code(db: AsyncSession, code: str) -> Optional[Language]:
    result = await db.execute(select(Language).where(Language.code == code))
    return result.scalar_one_or_none()


async def list_languages(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    family: Optional[str] = None,
    region: Optional[str] = None,
    is_written: Optional[bool] = None,
) -> List[Language]:
    query = select(Language).where(Language.is_active == True)  # noqa: E712
    if family:
        query = query.where(Language.family == family)
    if region:
        query = query.where(Language.region == region)
    if is_written is not None:
        query = query.where(Language.is_written == is_written)
    query = query.order_by(Language.name).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_language(db: AsyncSession, schema: LanguageCreate) -> Language:
    lang = Language(**schema.model_dump())
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


async def update_language(
    db: AsyncSession, language: Language, updates: LanguageUpdate
) -> Language:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(language, field, value)
    await db.commit()
    await db.refresh(language)
    return language
