"""Tutor and TutorRequest models."""

import enum
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TutorRequestStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"


class Tutor(Base):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # JSON array of language codes
    _specializations: Mapped[Optional[str]] = mapped_column(
        "specializations", Text, nullable=True, default="[]"
    )
    hourly_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="XAF", nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    years_experience: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    teaching_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="tutor_profile", lazy="select"
    )
    requests: Mapped[List["TutorRequest"]] = relationship(
        "TutorRequest", back_populates="tutor", lazy="select"
    )

    @property
    def specializations(self) -> List[str]:
        if self._specializations:
            try:
                return json.loads(self._specializations)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @specializations.setter
    def specializations(self, value: List[str]) -> None:
        self._specializations = json.dumps(value)


class TutorRequest(Base):
    __tablename__ = "tutor_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tutor_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tutors.id", ondelete="SET NULL"), nullable=True, index=True
    )
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False
    )
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TutorRequestStatus] = mapped_column(
        Enum(TutorRequestStatus), default=TutorRequestStatus.pending, nullable=False
    )
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    student: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="tutor_requests", foreign_keys=[student_id], lazy="select"
    )
    tutor: Mapped[Optional["Tutor"]] = relationship(
        "Tutor", back_populates="requests", lazy="select"
    )
    language: Mapped["Language"] = relationship(  # noqa: F821
        "Language", back_populates="tutor_requests", lazy="select"
    )
