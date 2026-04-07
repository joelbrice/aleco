"""Models package — imports all models so they are registered with Base.metadata."""

from app.models.user import User
from app.models.language import Language
from app.models.lesson import Lesson
from app.models.tutor import Tutor, TutorRequest
from app.models.conversation import AIConversation
from app.models.progress import UserProgress, UserStats

__all__ = [
    "User",
    "Language",
    "Lesson",
    "Tutor",
    "TutorRequest",
    "AIConversation",
    "UserProgress",
    "UserStats",
]
