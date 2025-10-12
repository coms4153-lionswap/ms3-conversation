# 🗨️ LionSwap Conversation & Messaging Service

**Author:** Wenhe(Kendall) Ma (wm2544@columbia.edu)  
**Course:** COMS W4153 – Cloud Computing & Containers  
**Sprint:** 1 – Service Skeleton & Deployment  
**Team Repo:** [https://github.com/coms4153-lionswap]

---

## 📖 Overview

This microservice is responsible for **one-to-one chat and messaging** between Columbia students on the LionSwap platform.  
It enables buyers and sellers to start conversations, send messages, and retrieve chat histories.

During **Sprint 1**, the service implements all RESTful API endpoints with placeholder logic (`NOT IMPLEMENTED`)  
and demonstrates working deployment on Google Cloud Platform.

---

## 🧩 Responsibilities

| Functionality                   | Description                                                                 |
| ------------------------------- | --------------------------------------------------------------------------- |
| **Conversations**               | Create and manage chat sessions between two users.                          |
| **Messages**                    | Send, retrieve, and list messages within a conversation.                    |
| **Future Expansion (Sprint 2)** | Add database persistence, timestamps, read status, and WebSocket live chat. |

---

## 🧱 Entities & Data Models

| Entity           | Description                                    | Key Fields                                                                     |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------------------------------ |
| **Conversation** | Represents a chat between two users.           | `conversation_id`, `user1_id`, `user2_id`, `created_at`, `last_message_at`     |
| **Message**      | Individual chat message within a conversation. | `message_id`, `conversation_id`, `sender_id`, `content`, `timestamp`, `status` |

All data models are defined using **Pydantic** in `models/conversation_models.py` and `models/message_models.py`.

---

## ⚙️ API Design

All endpoints follow the **RESTful** style.

| Method | Endpoint                           | Description                                         |
| ------ | ---------------------------------- | --------------------------------------------------- |
| `GET`  | `/conversations`                   | List all conversations (returns mock data)          |
| `POST` | `/conversations`                   | Create a new conversation (returns NOT IMPLEMENTED) |
| `GET`  | `/conversations/{conversation_id}` | Get details of a specific conversation              |
| `GET`  | `/messages`                        | List all messages (mock data)                       |
| `POST` | `/messages`                        | Send a new message (returns NOT IMPLEMENTED)        |
| `GET`  | `/messages/{message_id}`           | Retrieve message details                            |

➡️ All routes currently return placeholder responses as required by Sprint 1.

---

## 🧰 Run Locally

```bash
# Clone repo
git clone https://github.com/coms4153-lionswap.git
cd coms4153-lionswap/conversation-service

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
```
