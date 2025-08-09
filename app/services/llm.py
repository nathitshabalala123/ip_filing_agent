from typing import List
from openai import OpenAI
from ..config import settings
from ..schemas import ChatMessage

_SYSTEM_PROMPT = (
    "You are an AI assistant helping a user gather information to fill out South African CIPC trademark form TM1. "
    "You are not a lawyer and you do not provide legal advice, opinions, or predictions of success. "
    "Use simple, plain language. Ask only for information needed to complete the form. "
    "If asked for legal advice, decline and suggest consulting an attorney."
)

_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None


def triage_chat(messages: List[ChatMessage]) -> str:
    if _client is None:
        return (
            "OpenAI API key not configured. Please set OPENAI_API_KEY in your environment."
        )

    formatted_messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
    for m in messages:
        role = m.role if m.role in ("system", "user", "assistant") else "user"
        formatted_messages.append({"role": role, "content": m.content})
    
    try:
        completion = _client.chat.completions.create(
            model=settings.openai_model,
            messages=formatted_messages,
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:  # defensive: surface useful error message
        return (
            "Sorry, I could not process that request right now. "
            "Please try again in a moment. (Details: " + str(exc) + ")"
        )