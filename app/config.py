import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    app_env: str = os.getenv("APP_ENV", "development")
    generated_dir: str = os.getenv("GENERATED_DIR", "generated")

settings = Settings() 