import os
from datetime import datetime
from flask import Blueprint, request, send_file, jsonify
from ..services.pdf_generator import (
    generate_tm1_pdf,
    generate_poa_pdf,
    generate_filing_guide_pdf,
)
from ..utils.zipper import zip_files
from ..config import settings

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/generate', methods=['POST'])
def generate_documents():
    data = request.get_json()
    intake = data.get('intake')
    if not intake:
        return jsonify({"error": "Missing 'intake' in request body"}), 400

    tm1 = generate_tm1_pdf(intake)
    poa = generate_poa_pdf(intake)
    guide = generate_filing_guide_pdf(intake)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = os.path.join(settings.generated_dir, f"Trademark_Package_{timestamp}.zip")
    zip_path = zip_files([tm1, poa, guide], zip_name)

    return send_file(
        zip_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name=os.path.basename(zip_path),
    )