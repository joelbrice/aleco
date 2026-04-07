"""User model."""

import json
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_tutor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    native_language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # JSON array of language codes, stored as text
    _target_languages: Mapped[Optional[str]] = mapped_column(
        "target_languages", Text, nullable=True, default="[]"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    tutor_profile: Mapped[Optional["Tutor"]] = relationship(  # noqa: F821
        "Tutor", back_populates="user", uselist=False, lazy="select"
    )
    conversations: Mapped[List["AIConversation"]] = relationship(  # noqa: F821
        "AIConversation", back_populates="user", lazy="select"
    )
    progress_records: Mapped[List["UserProgress"]] = relationship(  # noqa: F821
        "UserProgress", back_populates="user", lazy="select"
    )
    stats: Mapped[Optional["UserStats"]] = relationship(  # noqa: F821
        "UserStats", back_populates="user", uselist=False, lazy="select"
    )
    tutor_requests: Mapped[List["TutorRequest"]] = relationship(  # noqa: F821
        "TutorRequest",
        back_populates="student",
        foreign_keys="TutorRequest.student_id",
        lazy="select",
    )

    @property
    def target_languages(self) -> List[str]:
        if self._target_languages:
            try:
                return json.loads(self._target_languages)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @target_languages.setter
    def target_languages(self, value: List[str]) -> None:
        self._target_languages = json.dumps(value)
