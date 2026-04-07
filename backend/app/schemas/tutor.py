"""Tutor schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.tutor import TutorRequestStatus
from app.schemas.user import UserPublic


class TutorBase(BaseModel):
    bio: Optional[str] = None
    specializations: List[str] = []
    hourly_rate: Optional[float] = None
    currency: str = "XAF"
    is_available: bool = True
    years_experience: Optional[int] = None
    teaching_style: Optional[str] = None


class TutorCreate(TutorBase):
    pass


class TutorUpdate(BaseModel):
    bio: Optional[str] = None
    specializations: Optional[List[str]] = None
    hourly_rate: Optional[float] = None
    currency: Optional[str] = None
    is_available: Optional[bool] = None
    years_experience: Optional[int] = None
    teaching_style: Optional[str] = None


class TutorResponse(TutorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    is_verified: bool
    rating: float
    total_reviews: int
    created_at: datetime
    user: Optional[UserPublic] = None


class TutorRequestCreate(BaseModel):
    language_id: int
    tutor_id: Optional[int] = None
    message: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class TutorRequestUpdate(BaseModel):
    status: TutorRequestStatus
    scheduled_at: Optional[datetime] = None


class TutorRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    tutor_id: Optional[int] = None
    language_id: int
    message: Optional[str] = None
    status: TutorRequestStatus
    scheduled_at: Optional[datetime] = None
    created_at: datetime
