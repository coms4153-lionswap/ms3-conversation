from fastapi import FastAPI, HTTPException
from typing import List
from sqlalchemy import text
from datetime import datetime

from database import engine
from models.conversation_models import ConversationCreate, ConversationRead
from models.message_models import MessageCreate, MessageRead

app = FastAPI(
    title="LionSwap Conversation & Messaging Service",
    description="Handles one-to-one chats between LionSwap users.",
    version="0.1-Sprint1",
)

# ============================================================
# 🩺 Health check
# ============================================================
@app.get("/health/db")
def health_check():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return {"db_ok": result.scalar() == 1}


# ============================================================
# 💬 Conversations Endpoints
# ============================================================

@app.get("/conversations", response_model=List[ConversationRead])
def list_conversations():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM Conversations ORDER BY conversation_id"))
        rows = [dict(row._mapping) for row in result]
    return rows


@app.post("/conversations", response_model=ConversationRead)
def create_conversation(conv: ConversationCreate):
    with engine.connect() as conn:
        # enforce user_a_id < user_b_id convention
        user_a_id, user_b_id = sorted([conv.user_a_id, conv.user_b_id])

        insert_stmt = text("""
            INSERT INTO Conversations (user_a_id, user_b_id)
            VALUES (:user_a_id, :user_b_id)
        """)
        result = conn.execute(insert_stmt, {"user_a_id": user_a_id, "user_b_id": user_b_id})
        conn.commit()

        conversation_id = result.lastrowid

        # fetch newly inserted row
        query = text("SELECT * FROM Conversations WHERE conversation_id = :cid")
        row = conn.execute(query, {"cid": conversation_id}).mappings().first()

    if not row:
        raise HTTPException(status_code=500, detail="Failed to create conversation")
    return dict(row)


@app.get("/conversations/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM Conversations WHERE conversation_id = :cid")
        row = conn.execute(query, {"cid": conversation_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return dict(row)


@app.put("/conversations/{conversation_id}", response_model=ConversationRead)
def update_conversation(conversation_id: int, conv: ConversationCreate):
    with engine.connect() as conn:
        stmt = text("""
            UPDATE Conversations
            SET user_a_id = :user_a_id,
                user_b_id = :user_b_id
            WHERE conversation_id = :cid
        """)
        conn.execute(stmt, {
            "user_a_id": conv.user_a_id,
            "user_b_id": conv.user_b_id,
            "cid": conversation_id,
        })
        conn.commit()

        row = conn.execute(
            text("SELECT * FROM Conversations WHERE conversation_id = :cid"),
            {"cid": conversation_id},
        ).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Conversation not found after update")
    return dict(row)


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM Conversations WHERE conversation_id = :cid"),
            {"cid": conversation_id},
        )
        conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": True, "conversation_id": conversation_id}


# ============================================================
# 📨 Messages Endpoints
# ============================================================

@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def list_messages(conversation_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM Messages
                WHERE conversation_id = :cid
                ORDER BY created_at ASC
            """),
            {"cid": conversation_id},
        )
        rows = [dict(row._mapping) for row in result]
    return rows


@app.post("/messages", response_model=MessageRead)
def create_message(msg: MessageCreate):
    with engine.connect() as conn:
        insert_stmt = text("""
            INSERT INTO Messages (conversation_id, sender_id, message_type, body, attachment_url)
            VALUES (:conversation_id, :sender_id, :message_type, :body, :attachment_url)
        """)
        result = conn.execute(insert_stmt, {
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "message_type": msg.message_type,
            "body": msg.body,
            "attachment_url": msg.attachment_url,
        })
        conn.commit()

        message_id = result.lastrowid

        # update conversation's last_message_at
        conn.execute(
            text("UPDATE Conversations SET last_message_at = NOW() WHERE conversation_id = :cid"),
            {"cid": msg.conversation_id},
        )
        conn.commit()

        row = conn.execute(
            text("SELECT * FROM Messages WHERE message_id = :mid"),
            {"mid": message_id},
        ).mappings().first()

    if not row:
        raise HTTPException(status_code=500, detail="Failed to create message")
    return dict(row)


@app.get("/messages/{message_id}", response_model=MessageRead)
def get_message(message_id: int):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM Messages WHERE message_id = :mid"),
            {"mid": message_id},
        ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Message not found")
    return dict(row)


@app.put("/messages/{message_id}", response_model=MessageRead)
def update_message(message_id: int, msg: MessageCreate):
    with engine.connect() as conn:
        stmt = text("""
            UPDATE Messages
            SET body = :body,
                message_type = :message_type,
                attachment_url = :attachment_url
            WHERE message_id = :mid
        """)
        result = conn.execute(stmt, {
            "body": msg.body,
            "message_type": msg.message_type,
            "attachment_url": msg.attachment_url,
            "mid": message_id,
        })
        conn.commit()

        row = conn.execute(
            text("SELECT * FROM Messages WHERE message_id = :mid"),
            {"mid": message_id},
        ).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Message not found after update")
    return dict(row)


@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM Messages WHERE message_id = :mid"),
            {"mid": message_id},
        )
        conn.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"deleted": True, "message_id": message_id}
