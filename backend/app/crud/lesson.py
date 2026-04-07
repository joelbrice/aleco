"""CRUD operations for Lesson."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson, LessonLevel, LessonType
from app.schemas.lesson import LessonCreate, LessonUpdate


async def get_lesson(db: AsyncSession, lesson_id: int) -> Optional[Lesson]:
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    return result.scalar_one_or_none()


async def list_lessons(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    language_id: Optional[int] = None,
    level: Optional[LessonLevel] = None,
    lesson_type: Optional[LessonType] = None,
    active_only: bool = True,
) -> List[Lesson]:
    query = select(Lesson)
    if active_only:
        query = query.where(Lesson.is_active == True)  # noqa: E712
    if language_id is not None:
        query = query.where(Lesson.language_id == language_id)
    if level is not None:
        query = query.where(Lesson.level == level)
    if lesson_type is not None:
        query = query.where(Lesson.lesson_type == lesson_type)
    query = query.order_by(Lesson.language_id, Lesson.order_index).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def list_lessons_for_language(
    db: AsyncSession, language_id: int, active_only: bool = True
) -> List[Lesson]:
    query = select(Lesson).where(Lesson.language_id == language_id)
    if active_only:
        query = query.where(Lesson.is_active == True)  # noqa: E712
    query = query.order_by(Lesson.order_index)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_lesson(db: AsyncSession, schema: LessonCreate) -> Lesson:
    data = schema.model_dump(exclude={"content"})
    lesson = Lesson(**data)
    lesson.content = schema.content
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


async def update_lesson(db: AsyncSession, lesson: Lesson, updates: LessonUpdate) -> Lesson:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "content":
            lesson.content = value
        else:
            setattr(lesson, field, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson
