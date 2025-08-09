from fastapi import APIRouter
from ..schemas import ConflictCheckRequest, ConflictCheckResponse
from ..services.conflict_check import basic_conflict_check, DISCLAIMER

router = APIRouter()


@router.post("/conflict-check", response_model=ConflictCheckResponse)
async def conflict_check(req: ConflictCheckRequest) -> ConflictCheckResponse:
    items = basic_conflict_check(req.mark_text, req.nice_classes)
    return ConflictCheckResponse(status="ok", disclaimer=DISCLAIMER, items=items) 