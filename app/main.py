from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes.chat import router as chat_router
from .routes.documents import router as documents_router
from .routes.classification import router as classification_router
from .routes.conflict import router as conflict_router

app = FastAPI(
    title="IP Filing Co-Pilot (ZA)",
    description="Assistive tool for preparing CIPC trademark filing packages. Not a law firm.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/triage", tags=["triage"])
app.include_router(classification_router, prefix="/api/classify", tags=["classification"])
app.include_router(conflict_router, prefix="/api", tags=["conflict-check"])
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])

@app.get("/")
async def health() -> dict:
    return {"status": "ok", "env": settings.app_env} 