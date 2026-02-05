from fastapi import APIRouter, Depends
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
import time

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.get("/", summary="Obtener Transacciones", description="Obtener historial de transacciones")
async def get_transactions(limit: int = 10, current_user: str = Depends(get_current_user)):
    time.sleep(0.5)
    transactions = MOCK_DATA["transactions"].get(current_user, [])
    return {"success": True, "transactions": transactions[:limit]}
