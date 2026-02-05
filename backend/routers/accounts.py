from fastapi import APIRouter, Depends
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
import time

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

@router.get("/", summary="Obtener Cuentas", description="Obtener las cuentas del usuario actual")
async def get_accounts(current_user: str = Depends(get_current_user)):
    time.sleep(0.4)
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    return {"success": True, "accounts": accounts}
