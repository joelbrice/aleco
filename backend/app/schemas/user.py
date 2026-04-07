"""User schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    native_language: Optional[str] = None
    target_languages: List[str] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    native_language: Optional[str] = None
    target_languages: Optional[List[str]] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_verified: bool
    is_tutor: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserPublic(BaseModel):
    """Public-facing user info (limited fields)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_tutor: bool
    created_at: datetime
