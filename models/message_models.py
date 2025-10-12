from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from typing import Annotated
from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class MessageBase(BaseModel):
    conversation_id: UUID = Field(
        ...,
        description="FK to ConversationRead.conversation_id.",
        json_schema_extra={"example": "aaaa1111-bbbb-4ccc-8ddd-eeeeeeeeeeee"},
    )
    sender_id: UUID = Field(
        ...,
        description="UUID of the sender.",
        json_schema_extra={"example": "11111111-1111-4111-8111-111111111111"},
    )
    content: Annotated[str, StringConstraints(min_length=1, max_length=1000)] = Field(
        ...,
        description="Message body content.",
        json_schema_extra={"example": "Hi, is this item still available?"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": "aaaa1111-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                    "sender_id": "11111111-1111-4111-8111-111111111111",
                    "content": "Hi, is this item still available?"
                }
            ]
        }
    }


class MessageCreate(MessageBase):
    """Payload for creating a new message (Sprint 1)."""
    pass


class MessageRead(MessageBase):
    message_id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated message ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message timestamp (UTC).",
        json_schema_extra={"example": "2025-10-11T20:01:30Z"},
    )
