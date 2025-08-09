from fastapi import APIRouter
from ..schemas import ClassificationRequest, ClassificationResponse, ClassificationSuggestion
from ..services.classification import suggest_classes

router = APIRouter()


@router.post("/suggest", response_model=ClassificationResponse)
async def suggest(req: ClassificationRequest) -> ClassificationResponse:
    raw = suggest_classes(req.business_description)
    suggestions = [
        ClassificationSuggestion(
            class_number=cn, class_title=title, confidence=conf
        )
        for (cn, title, conf) in raw
    ]
    return ClassificationResponse(suggestions=suggestions) 