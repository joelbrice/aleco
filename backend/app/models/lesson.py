"""Lesson model."""

import enum
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LessonType(str, enum.Enum):
    vocabulary = "vocabulary"
    phrases = "phrases"
    grammar = "grammar"
    conversation = "conversation"
    pronunciation = "pronunciation"
    culture = "culture"


class LessonLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    lesson_type: Mapped[LessonType] = mapped_column(
        Enum(LessonType), default=LessonType.vocabulary, nullable=False
    )
    level: Mapped[LessonLevel] = mapped_column(
        Enum(LessonLevel), default=LessonLevel.beginner, nullable=False
    )
    # JSON content stored as text
    _content: Mapped[Optional[str]] = mapped_column("content", Text, nullable=True)
    audio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    language: Mapped["Language"] = relationship(  # noqa: F821
        "Language", back_populates="lessons", lazy="select"
    )
    progress_records: Mapped[List["UserProgress"]] = relationship(  # noqa: F821
        "UserProgress", back_populates="lesson", lazy="select"
    )

    @property
    def content(self) -> Optional[Dict[str, Any]]:
        if self._content:
            try:
                return json.loads(self._content)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    @content.setter
    def content(self, value: Optional[Dict[str, Any]]) -> None:
        self._content = json.dumps(value) if value is not None else None
