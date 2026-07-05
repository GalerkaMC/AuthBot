"""
FastAPI роутер
"""


from datetime import datetime

from fastapi import APIRouter

from backend.models import AuthRequest

router = APIRouter()

@router.get("/api/v1/health/")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}

@router.post("/api/v1/2fa/")
def request_2fa(request: AuthRequest):
    """Initiate 2FA process"""
    # Placeholder logic – in real bot, send Telegram message etc.
    return {"status": "pending", "message": "Authorization request sent to user"}
