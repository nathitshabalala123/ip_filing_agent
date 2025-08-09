from fastapi import APIRouter
from ..schemas import ChatRequest
from ..services.llm import triage_chat

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> dict:
    reply = triage_chat(req.messages)
    return {"reply": reply} 