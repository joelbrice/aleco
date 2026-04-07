"""Language model."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    native_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="Cameroon", nullable=False)
    family: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    is_written: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    script: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    speaker_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    audio_resources_available: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(  # noqa: F821
        "Lesson", back_populates="language", lazy="select"
    )
    conversations: Mapped[List["AIConversation"]] = relationship(  # noqa: F821
        "AIConversation", back_populates="language", lazy="select"
    )
    tutor_requests: Mapped[List["TutorRequest"]] = relationship(  # noqa: F821
        "TutorRequest", back_populates="language", lazy="select"
    )
    progress_records: Mapped[List["UserProgress"]] = relationship(  # noqa: F821
        "UserProgress", back_populates="language", lazy="select"
    )
