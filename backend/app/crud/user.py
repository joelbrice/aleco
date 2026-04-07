"""CRUD operations for User."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, schema: UserCreate) -> User:
    user = User(
        email=schema.email,
        username=schema.username,
        hashed_password=hash_password(schema.password),
        full_name=schema.full_name,
        native_language=schema.native_language,
    )
    user.target_languages = []
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def update_user(db: AsyncSession, user: User, updates: UserUpdate) -> User:
    data = updates.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "target_languages":
            user.target_languages = value
        else:
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user
