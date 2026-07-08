"""
FastAPI роутер
"""



from datetime import datetime

from fastapi import APIRouter

from src.backend.two_factor_authentication.entities import TwoFAEntitiesManager
from src.backend.two_factor_authentication.entities.TwoFAEntity import TwoFAEntity
from src.backend.two_factor_authentication.server.models import AuthRequest

router = APIRouter()

@router.get("/api/v1/health/")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}


@router.post("/api/v1/2fa")
async def request_2fa(request: AuthRequest):
    """2FA for player enpoint"""

    user_id = int(request.userId)

    entity = TwoFAEntity(request.nickname, int(user_id))
    TwoFAEntitiesManager().add(user_id, entity)

    await entity.send_2fa_message()

    return {"status": 200}