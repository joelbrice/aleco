"""Lesson schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.lesson import LessonLevel, LessonType


class VocabItem(BaseModel):
    target: str
    translation: str
    phonetic: Optional[str] = None
    audio_hint: Optional[str] = None
    example_sentence: Optional[str] = None
    example_translation: Optional[str] = None
    cultural_note: Optional[str] = None


class LessonContent(BaseModel):
    items: Optional[List[VocabItem]] = None
    text: Optional[str] = None
    sections: Optional[List[Dict[str, Any]]] = None
    quiz_questions: Optional[List[Dict[str, Any]]] = None


class LessonBase(BaseModel):
    language_id: int
    title: str
    description: Optional[str] = None
    lesson_type: LessonType = LessonType.vocabulary
    level: LessonLevel = LessonLevel.beginner
    content: Optional[Dict[str, Any]] = None
    audio_url: Optional[str] = None
    order_index: int = 0
    xp_reward: int = 10


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    lesson_type: Optional[LessonType] = None
    level: Optional[LessonLevel] = None
    content: Optional[Dict[str, Any]] = None
    audio_url: Optional[str] = None
    order_index: Optional[int] = None
    xp_reward: Optional[int] = None
    is_active: Optional[bool] = None


class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    language_id: int
    title: str
    description: Optional[str] = None
    lesson_type: LessonType
    level: LessonLevel
    content: Optional[Dict[str, Any]] = None
    audio_url: Optional[str] = None
    order_index: int
    xp_reward: int
    is_active: bool
    created_at: datetime


class LessonSummary(BaseModel):
    """Lesson without full content for listing."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    language_id: int
    title: str
    description: Optional[str] = None
    lesson_type: LessonType
    level: LessonLevel
    order_index: int
    xp_reward: int
    is_active: bool


class CompleteLesson(BaseModel):
    score: int = 100


class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_index: int
    explanation: Optional[str] = None
