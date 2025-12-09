from fastapi import FastAPI, HTTPException, Header, Response
from typing import List, Optional #
from sqlalchemy import text
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor
import uuid
from datetime import datetime
from fastapi import HTTPException
from fastapi import Depends
from auth_utils import verify_token



# Thread pool with 4 worker threads (you can change to 2 or 8)
executor = ThreadPoolExecutor(max_workers=4)

# In-memory task status store
TASK_STATUS = {}

from database import engine
from models.conversation_models import ConversationCreate, ConversationRead
from models.message_models import MessageCreate, MessageRead
from fastapi.middleware.cors import CORSMiddleware

def run_heavy_task(task_id: str, conversation_id: int):
    """
    Heavy background job executed inside a worker thread.
    """
    TASK_STATUS[task_id] = {
        "status": "running",
        "started_at": datetime.utcnow()
    }

    # simulate expensive computation (NLP, DB aggregation, etc)
    time.sleep(20)

    TASK_STATUS[task_id] = {
        "status": "completed",
        "completed_at": datetime.utcnow(),
        "result": f"Summary for conversation {conversation_id} generated."
    }

app = FastAPI(
    title="LionSwap Conversation & Messaging Service",
    description="Handles one-to-one chats between LionSwap users.",
    version="0.1-Sprint1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://storage.googleapis.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/health/db")
def health_check():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return {"db_ok": result.scalar() == 1}


# ============================================================
# Conversations Endpoints
# ============================================================


@app.get("/conversations")
def get_conversations(user = Depends(verify_token)):
    user_id = user["user_id"]
    role = user["role"]

    with engine.connect() as conn:
        if role == "admin":
            result = conn.execute(text("SELECT * FROM conversations"))
        else:
            result = conn.execute(
                text("SELECT * FROM conversations WHERE user1_id=:uid OR user2_id=:uid"),
                {"uid": user_id}
            )

        return {"conversations": [dict(row) for row in result]}

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
# Messages Endpoints
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


# 4. 修复：正确添加 response 和 if_none_match 参数
@app.get("/messages/{message_id}", response_model=MessageRead)
def get_message(
    message_id: int, 
    response: Response, 
    if_none_match: Optional[str] = Header(None)
):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM Messages WHERE message_id = :mid"),
            {"mid": message_id},
        ).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message_dict = dict(row)
    etag_value = f"W/{hash(frozenset(message_dict.items()))}"

    if if_none_match == etag_value:
        response.status_code = 304
        return response

    response.headers["ETag"] = etag_value
    return message_dict


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
# ============================================================
# Async job trigger (202 Accepted)
# ============================================================

@app.post("/conversations/{conversation_id}/build-summary", status_code=202)
def build_summary(conversation_id: int):
   
    task_id = str(uuid.uuid4())

    TASK_STATUS[task_id] = {
        "status": "queued",
        "created_at": datetime.utcnow()
    }
    executor.submit(run_heavy_task, task_id, conversation_id)

    return {
        "detail": "Job accepted.",
        "task_id": task_id,
        "poll_url": f"/tasks/{task_id}"
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    if task_id not in TASK_STATUS:
        raise HTTPException(status_code=404, detail="Unknown task ID.")
    return TASK_STATUS[task_id]