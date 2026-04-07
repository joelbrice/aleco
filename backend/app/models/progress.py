"""UserProgress and UserStats models."""

import enum
import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[ProgressStatus] = mapped_column(
        Enum(ProgressStatus), default=ProgressStatus.not_started, nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="progress_records", lazy="select"
    )
    language: Mapped["Language"] = relationship(  # noqa: F821
        "Language", back_populates="progress_records", lazy="select"
    )
    lesson: Mapped["Lesson"] = relationship(  # noqa: F821
        "Lesson", back_populates="progress_records", lazy="select"
    )


class UserStats(Base):
    __tablename__ = "user_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # JSON array of language codes currently being learned
    _languages_learning: Mapped[Optional[str]] = mapped_column(
        "languages_learning", Text, nullable=True, default="[]"
    )
    lessons_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="stats", lazy="select"
    )

    @property
    def level(self) -> int:
        """Compute level from total XP. Every 500 XP is a new level."""
        return max(1, self.total_xp // 500 + 1)

    @property
    def languages_learning(self) -> List[str]:
        if self._languages_learning:
            try:
                return json.loads(self._languages_learning)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @languages_learning.setter
    def languages_learning(self, value: List[str]) -> None:
        self._languages_learning = json.dumps(value)
