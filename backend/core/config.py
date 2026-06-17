from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


class Settings:
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        if database_url and database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1
            )
        self.DATABASE_URL = database_url
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
        self.FRONTEND_URL = os.getenv(
            "FRONTEND_URL", "http://localhost:5173"
        )
        self.CORS_ORIGINS = _split_csv(
            os.getenv("CORS_ORIGINS")
        ) or [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ]
        self.AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    def validate_database(self):
        if not self.DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL is required. Set it in backend/.env "
                "or the deployment environment."
            )

    def validate_frontend(self):
        if not self.FRONTEND_URL and not self.CORS_ORIGINS:
            raise RuntimeError(
                "FRONTEND_URL or CORS_ORIGINS must be set for CORS."
            )

    def validate_security(self):
        if not self.SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY is required. Set it in backend/.env "
                "or the deployment environment."
            )
        if not self.ENCRYPTION_KEY:
            raise RuntimeError(
                "ENCRYPTION_KEY is required. Generate one with: "
                "python -c \"from cryptography.fernet import Fernet; "
                "print(Fernet.generate_key().decode())\""
            )


settings = Settings()
