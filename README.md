## IP Filing Co-Pilot (South Africa) - Backend MVP

This is a FastAPI backend for an AI "Co-Pilot" that guides users through preparing a South African trademark filing package for self-filing on the CIPC portal. It avoids providing legal advice and focuses on intake, basic class suggestion, a simple name conflict check stub, and PDF document generation (TM1, POA, Filing Guide) into a ZIP for download.

### Key Notes
- Not a law firm. No legal advice is provided.
- Uses OpenAI model `gpt-5` via `OPENAI_API_KEY`.
- No direct integration with CIPC filing. Users self-file on CIPC.

### Tech Stack
- FastAPI, Uvicorn
- OpenAI API
- ReportLab for PDF generation
- httpx (placeholder for public conflict search)

### Setup
1) Python 3.11+
2) Create and activate a virtual environment
   - Windows PowerShell:
     ```powershell
     py -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3) Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4) Configure environment
   - Copy `.env.example` to `.env`
   - Set `OPENAI_API_KEY` to your key
   - Optionally set `OPENAI_MODEL` (defaults to `gpt-5`)

5) Run the server
   ```bash
   uvicorn app.main:app --reload
   ```
6) Open API docs: http://127.0.0.1:8000/docs

### Environment Variables
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (default: `gpt-4o`)
- `APP_ENV` (default: `development`)

### Endpoints (MVP)
- `POST /api/triage/chat` — Conversational intake (strict disclaimers)
- `POST /api/classify/suggest` — Suggest NICE classes from a business description
- `POST /api/conflict-check` — Basic name check (stubbed)
- `POST /api/documents/generate` — Generates TM1, POA, and a Filing Guide PDFs and returns a ZIP

### Disclaimers
This software is provided for educational and operational assistance only and is not legal advice. Users must review and accept Terms of Service that clearly state this system is not a law firm and does not replace an attorney. 