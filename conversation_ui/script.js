const API_BASE = "http://127.0.0.1:8000" // e.g., https://lionswap-ms3-xyz.a.run.app

const convInput = document.getElementById("conversation-id")
const senderInput = document.getElementById("sender-id")
const msgInput = document.getElementById("message-input")
const msgContainer = document.getElementById("messages")

let conversationId = null
let senderId = null

document.getElementById("load-btn").addEventListener("click", loadMessages)
document.getElementById("send-btn").addEventListener("click", sendMessage)

async function loadMessages () {
  conversationId = parseInt(convInput.value)
  senderId = parseInt(senderInput.value)
  if (!conversationId || !senderId) {
    alert("Enter both conversation ID and your user ID!")
    return
  }

  msgContainer.innerHTML = "<em>Loading...</em>"

  const res = await fetch(`${API_BASE}/conversations/${conversationId}/messages`)
  const messages = await res.json()
  renderMessages(messages)
}

function renderMessages (messages) {
  msgContainer.innerHTML = ""
  messages.forEach((m) => {
    const div = document.createElement("div")
    div.classList.add("message")
    div.classList.add(m.sender_id === senderId ? "sent" : "received")
    div.textContent = m.body
    msgContainer.appendChild(div)
  })
  msgContainer.scrollTop = msgContainer.scrollHeight
}

async function sendMessage () {
  const body = msgInput.value.trim()
  if (!body) return

  const msg = {
    conversation_id: conversationId,
    sender_id: senderId,
    message_type: "TEXT",
    body,
    attachment_url: null,
  }

  const res = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(msg),
  })

  if (res.ok) {
    const newMsg = await res.json()
    renderMessages([...document.querySelectorAll(".message")].map(d => d.textContent).concat(newMsg))
    msgInput.value = ""
    loadMessages() // refresh list
  } else {
    alert("Failed to send message")
  }
}
