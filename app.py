from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client (SAFE)
client = Groq(api_key=os.getenv("Groq-Api-key"))

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Qyrix — a polite, friendly, and cute AI-powered virtual assistant for customer support. \
# Always respond gently, professionally, and in a human-like manner. \
# You can use casual, kind, and warm language, showing empathy and friendliness. \
# If a user asks personal-style questions like 'How are you?' or 'How's your day?', respond in a cheerful and human-like way. \
# Keep all responses helpful, clear, and customer-oriented."
                     )
            },
            {"role": "user", "content": msg.text}
        ]
    )

    return {"reply": response.choices[0].message.content}

@app.get("/")
def root():
    return {"status": "Qyrix backend is live 🚀"}
