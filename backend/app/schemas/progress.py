"""Progress schemas."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.progress import ProgressStatus


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    language_id: int
    lesson_id: int
    status: ProgressStatus
    score: int
    xp_earned: int
    completed_at: Optional[datetime] = None
    created_at: datetime


class StatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_xp: int
    current_streak: int
    longest_streak: int
    languages_learning: List[str] = []
    lessons_completed: int
    last_activity_date: Optional[date] = None
    level: int


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date] = None


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    total_xp: int
    level: int
    lessons_completed: int
