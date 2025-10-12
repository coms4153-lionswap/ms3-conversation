from fastapi import FastAPI
from typing import List
from uuid import UUID

from models.conversation_models import ConversationCreate, ConversationRead
from models.message_models import MessageCreate, MessageRead

app = FastAPI(
    title="LionSwap Conversation & Messaging Service",
    description="Handles one-to-one chats between LionSwap users.",
    version="0.1-Sprint1",
)

# ---------- Conversations ----------

@app.get("/conversations", response_model=List[ConversationRead])
def list_conversations():
    return [{"status": "NOT IMPLEMENTED"}]

@app.post("/conversations", response_model=ConversationRead)
def create_conversation(conv: ConversationCreate):
    return {"status": "NOT IMPLEMENTED"}

@app.get("/conversations/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: UUID):
    return {"status": "NOT IMPLEMENTED"}

@app.put("/conversations/{conversation_id}", response_model=ConversationRead)
def update_conversation(conversation_id: UUID, conv: ConversationCreate):
    return {"status": "NOT IMPLEMENTED"}

@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: UUID):
    return {"status": "NOT IMPLEMENTED"}

# ---------- Messages ----------

@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def list_messages(conversation_id: UUID):
    return [{"status": "NOT IMPLEMENTED"}]

@app.post("/messages", response_model=MessageRead)
def create_message(msg: MessageCreate):
    return {"status": "NOT IMPLEMENTED"}

@app.get("/messages/{message_id}", response_model=MessageRead)
def get_message(message_id: UUID):
    return {"status": "NOT IMPLEMENTED"}

@app.put("/messages/{message_id}", response_model=MessageRead)
def update_message(message_id: UUID, msg: MessageCreate):
    return {"status": "NOT IMPLEMENTED"}

@app.delete("/messages/{message_id}")
def delete_message(message_id: UUID):
    return {"status": "NOT IMPLEMENTED"}
