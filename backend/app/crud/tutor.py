"""CRUD operations for Tutor and TutorRequest."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.tutor import Tutor, TutorRequest, TutorRequestStatus
from app.schemas.tutor import TutorCreate, TutorRequestCreate, TutorRequestUpdate, TutorUpdate


async def get_tutor(db: AsyncSession, tutor_id: int) -> Optional[Tutor]:
    result = await db.execute(
        select(Tutor).where(Tutor.id == tutor_id).options(selectinload(Tutor.user))
    )
    return result.scalar_one_or_none()


async def get_tutor_by_user_id(db: AsyncSession, user_id: int) -> Optional[Tutor]:
    result = await db.execute(select(Tutor).where(Tutor.user_id == user_id))
    return result.scalar_one_or_none()


async def list_tutors(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    language_code: Optional[str] = None,
    available_only: bool = False,
) -> List[Tutor]:
    query = select(Tutor).options(selectinload(Tutor.user))
    if available_only:
        query = query.where(Tutor.is_available == True)  # noqa: E712
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    tutors = list(result.scalars().all())
    if language_code:
        tutors = [t for t in tutors if language_code in t.specializations]
    return tutors


async def create_tutor(db: AsyncSession, user_id: int, schema: TutorCreate) -> Tutor:
    data = schema.model_dump(exclude={"specializations"})
    tutor = Tutor(user_id=user_id, **data)
    tutor.specializations = schema.specializations
    db.add(tutor)
    await db.commit()
    await db.refresh(tutor)
    return tutor


async def update_tutor(db: AsyncSession, tutor: Tutor, updates: TutorUpdate) -> Tutor:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "specializations":
            tutor.specializations = value
        else:
            setattr(tutor, field, value)
    await db.commit()
    await db.refresh(tutor)
    return tutor


async def create_tutor_request(
    db: AsyncSession, student_id: int, schema: TutorRequestCreate
) -> TutorRequest:
    req = TutorRequest(
        student_id=student_id,
        tutor_id=schema.tutor_id,
        language_id=schema.language_id,
        message=schema.message,
        scheduled_at=schema.scheduled_at,
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def get_tutor_request(db: AsyncSession, request_id: int) -> Optional[TutorRequest]:
    result = await db.execute(
        select(TutorRequest).where(TutorRequest.id == request_id)
    )
    return result.scalar_one_or_none()


async def list_tutor_requests_for_student(
    db: AsyncSession, student_id: int
) -> List[TutorRequest]:
    result = await db.execute(
        select(TutorRequest)
        .where(TutorRequest.student_id == student_id)
        .order_by(TutorRequest.created_at.desc())
    )
    return list(result.scalars().all())


async def update_tutor_request(
    db: AsyncSession, req: TutorRequest, updates: TutorRequestUpdate
) -> TutorRequest:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(req, field, value)
    await db.commit()
    await db.refresh(req)
    return req
