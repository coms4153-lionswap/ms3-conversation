# 🗨️ LionSwap Conversation & Messaging Service

**Author:** Wenhe(Kendall) Ma (wm2544@columbia.edu)  
**Course:** COMS W4153 – Cloud Computing & Containers  
**Sprint:** 1 – Service Skeleton & Deployment  
**Team Repo:** [https://github.com/coms4153-lionswap]

---

## 📖 Overview

This microservice is responsible for **one-to-one chat and messaging** between Columbia students on the LionSwap platform.  
It enables buyers and sellers to start conversations, send messages, and retrieve chat histories. This microservice is successfully deployed on a vm on google cloud.

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

## ☁️ Deployment Details

**Deployed on:** Google Cloud Platform (Compute Engine)  
**VM Name:** lionswap-conversation-vm  
**Region:** us-central1-c  
**Instance Type:** e2-micro (Ubuntu 22.04 LTS)  
**Firewall Port:** TCP 8000

**Public URL:**  
 [http://35.227.121.98:8000/docs](http://35.227.121.98:8000/docs)

**Status:** Running

### Commands Used

```bash
sudo apt update -y
sudo apt install python3-venv git -y
git clone https://github.com/wenhema/lionswap-conversation-service.git
cd lionswap-conversation-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --break-system-packages
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
