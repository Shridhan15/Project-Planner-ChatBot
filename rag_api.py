from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_chat import rag_query   # Function from rag_chat.py

app = FastAPI()

# CORS (allow all for frontend/backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Body model
class ChatRequest(BaseModel):
    query: str

# Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    response = rag_query(req.query)
    return {"answer": response}

@app.get("/")
def home():
    return {"message": "ProjectPartner RAG API is running"}
