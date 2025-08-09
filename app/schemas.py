from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class ChatMessage(BaseModel):
    role: str  # "system" | "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(default_factory=list)


class ClassificationRequest(BaseModel):
    business_description: str


class ClassificationSuggestion(BaseModel):
    class_number: int
    class_title: str
    confidence: float


class ClassificationResponse(BaseModel):
    suggestions: List[ClassificationSuggestion]


class ApplicantDetails(BaseModel):
    full_name: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    province: str
    postal_code: str
    country: str = "South Africa"
    email: EmailStr
    phone_number: str


class TrademarkIntake(BaseModel):
    mark_text: str
    nice_classes: List[int]
    applicant: ApplicantDetails
    slogan: Optional[str] = None


class ConflictCheckRequest(BaseModel):
    mark_text: str
    nice_classes: List[int]


class ConflictItem(BaseModel):
    mark_text: str
    class_number: int
    similarity: float
    source_url: Optional[str] = None


class ConflictCheckResponse(BaseModel):
    status: str
    disclaimer: str
    items: List[ConflictItem] = Field(default_factory=list)


class DocumentGenerateRequest(BaseModel):
    intake: TrademarkIntake


class DocumentGenerateResponse(BaseModel):
    zip_filename: str
    message: str 