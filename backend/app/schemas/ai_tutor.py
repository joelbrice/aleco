"""AI Tutor schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class AIPersona(BaseModel):
    language_code: str
    language_name: str
    persona_name: str
    persona_description: str
    avatar_hint: Optional[str] = None


class ConversationCreate(BaseModel):
    language_id: int


class MessageCreate(BaseModel):
    content: str


class ConversationMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: str
    audio_url: Optional[str] = None


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    language_id: int
    persona_name: str
    persona_description: Optional[str] = None
    messages: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime


class ConversationSummary(BaseModel):
    """Conversation without full message history."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    language_id: int
    persona_name: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0


class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    role: str = "assistant"
