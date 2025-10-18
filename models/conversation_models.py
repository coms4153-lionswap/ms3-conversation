from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class ConversationBase(BaseModel):
    user_a_id: int = Field(
        ...,
        description="Smaller user ID in the pair (user_a_id < user_b_id).",
        json_schema_extra={"example": 1},
    )
    user_b_id: int = Field(
        ...,
        description="Larger user ID in the pair (user_a_id < user_b_id).",
        json_schema_extra={"example": 2},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_a_id": 1,
                    "user_b_id": 2,
                }
            ]
        }
    }



class ConversationCreate(ConversationBase):
    """Payload for creating a new conversation."""
    pass

class ConversationRead(ConversationBase):
    conversation_id: int = Field(
        ...,
        description="Auto-incremented ID of the conversation.",
        json_schema_extra={"example": 10},
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the conversation was created (UTC).",
        json_schema_extra={"example": "2025-10-13T16:36:27Z"},
    )
    last_message_at: datetime | None = Field(
        default=None,
        description="Timestamp of the most recent message in this conversation (UTC).",
        json_schema_extra={"example": "2025-10-14T08:22:10Z"},
    )

    class Config:
        orm_mode = True
