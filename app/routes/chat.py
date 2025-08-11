from fastapi import APIRouter
from ..schemas import ChatRequest
from ..services.llm import triage_chat
from flask import Blueprint

router = APIRouter()
chat_bp = Blueprint('chat', __name__)


@router.post("/chat")
async def chat(req: ChatRequest) -> dict:
    reply = triage_chat(req.messages)
    return {"reply": reply}


@chat_bp.route('/', methods=['GET'])
def chat_root():
    return {"message": "Chat root"}