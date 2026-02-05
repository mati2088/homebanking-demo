from fastapi import APIRouter, Depends
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
import time

router = APIRouter(prefix="/sistema", tags=["Sistema"])

@router.post("/resetear", summary="Resetear Sistema", description="Restablecer datos del simulador a su estado inicial")
async def reset_data(current_user: str = Depends(get_current_user)):
    time.sleep(1.5)
    # Reset critical balances for demo
    if current_user in MOCK_DATA["accounts"]:
        accounts = MOCK_DATA["accounts"][current_user]
        if len(accounts) > 0: accounts[0]["balance"] = 500000.00
        if len(accounts) > 1: accounts[1]["balance"] = 250000.00
        # Reset credit card limit availability logic is a bit complex in mock, skipping precise reset for simplicity
        
    return {"success": True, "message": "Simulador restablecido: Fondos recargados"}
