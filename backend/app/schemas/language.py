"""Language schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LanguageBase(BaseModel):
    code: str
    name: str
    native_name: Optional[str] = None
    region: Optional[str] = None
    country: str = "Cameroon"
    family: Optional[str] = None
    is_written: bool = True
    script: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: int = 3
    speaker_count: Optional[int] = None
    audio_resources_available: bool = False


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(BaseModel):
    name: Optional[str] = None
    native_name: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[int] = None
    is_active: Optional[bool] = None
    audio_resources_available: Optional[bool] = None


class LanguageResponse(LanguageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


class LanguageStatsResponse(BaseModel):
    language_code: str
    language_name: str
    total_lessons: int
    total_learners: int
    lessons_completed: int
    avg_score: float
