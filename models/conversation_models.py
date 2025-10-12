from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
    user1_id: UUID = Field(
        ...,
        description="UUID of the first participant (e.g., seller).",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    user2_id: UUID = Field(
        ...,
        description="UUID of the second participant (e.g., buyer).",
        json_schema_extra={"example": "22222222-2222-4222-8222-222222222222"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user1_id": "11111111-1111-4111-8111-111111111111",
                    "user2_id": "22222222-2222-4222-8222-222222222222",
                }
            ]
        }
    }


class ConversationCreate(ConversationBase):
    """Payload for creating a new conversation (Sprint 1)."""
    pass


class ConversationRead(ConversationBase):
    conversation_id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated conversation ID.",
        json_schema_extra={"example": "aaaa1111-bbbb-4ccc-8ddd-eeeeeeeeeeee"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp (UTC).",
        json_schema_extra={"example": "2025-10-11T20:00:00Z"},
    )
