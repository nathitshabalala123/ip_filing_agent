import os
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..schemas import DocumentGenerateRequest
from ..services.pdf_generator import (
    generate_tm1_pdf,
    generate_poa_pdf,
    generate_filing_guide_pdf,
)
from ..utils.zipper import zip_files
from ..config import settings

router = APIRouter()


@router.post("/generate")
async def generate_documents(req: DocumentGenerateRequest):
    tm1 = generate_tm1_pdf(req.intake.model_dump())
    poa = generate_poa_pdf(req.intake.model_dump())
    guide = generate_filing_guide_pdf(req.intake.model_dump())

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = os.path.join(settings.generated_dir, f"Trademark_Package_{timestamp}.zip")
    zip_path = zip_files([tm1, poa, guide], zip_name)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=os.path.basename(zip_path),
    ) 