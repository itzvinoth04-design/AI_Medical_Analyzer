import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "SQLITE#.db"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mediguide-ai-rec-super-secret-key-2026")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "mediguide-ai-jwt-rec-2026")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = 24
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CORS_HEADERS = "Content-Type"
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    REPORTS_FOLDER = BASE_DIR / "reports"

os.makedirs(BASE_DIR / "database", exist_ok=True)
os.makedirs(BASE_DIR / "uploads", exist_ok=True)
os.makedirs(BASE_DIR / "reports", exist_ok=True)
