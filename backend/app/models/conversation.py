"""AIConversation model."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    persona_name: Mapped[str] = mapped_column(String(100), nullable=False)
    persona_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # JSON array of message objects
    _messages: Mapped[Optional[str]] = mapped_column("messages", Text, nullable=True, default="[]")

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
    user: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="conversations", lazy="select"
    )
    language: Mapped["Language"] = relationship(  # noqa: F821
        "Language", back_populates="conversations", lazy="select"
    )

    @property
    def messages(self) -> List[Dict[str, Any]]:
        if self._messages:
            try:
                return json.loads(self._messages)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @messages.setter
    def messages(self, value: List[Dict[str, Any]]) -> None:
        self._messages = json.dumps(value)
