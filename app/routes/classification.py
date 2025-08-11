from fastapi import APIRouter
from flask import Blueprint, request, jsonify
from ..schemas import ClassificationRequest, ClassificationResponse, ClassificationSuggestion
from ..services.classification import suggest_classes

router = APIRouter()
classification_bp = Blueprint('classification', __name__)


@router.post("/classification")
async def chat(req: ChatRequest) -> dict:
    reply = triage_chat(req.messages)
    return {"reply": reply}


@classification_bp.route('/', methods=['GET'])
def classification_root():
    return jsonify({"message": "Classification API root"})


@classification_bp.route('/suggest', methods=['POST'])
def classify():
    data = request.get_json()
    # You may want to validate 'data' here
    suggestions = suggest_classes(data)
    return jsonify({"suggestions": suggestions})