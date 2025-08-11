from fastapi import APIRouter
from ..schemas import ConflictCheckRequest, ConflictCheckResponse
from ..services.conflict_check import basic_conflict_check, DISCLAIMER
from flask import Blueprint, request, jsonify

router = APIRouter()
conflict_bp = Blueprint('conflict', __name__)


@router.post("/conflict-check", response_model=ConflictCheckResponse)
async def conflict_check(req: ConflictCheckRequest) -> ConflictCheckResponse:
    items = basic_conflict_check(req.mark_text, req.nice_classes)
    return ConflictCheckResponse(status="ok", disclaimer=DISCLAIMER, items=items)


@conflict_bp.route('/conflict-check', methods=['POST'])
def conflict_check():
    data = request.get_json()
    mark_text = data.get('mark_text')
    nice_classes = data.get('nice_classes')
    items = basic_conflict_check(mark_text, nice_classes)
    return jsonify({
        "status": "ok",
        "disclaimer": DISCLAIMER,
        "items": items
    })