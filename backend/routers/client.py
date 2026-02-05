from fastapi import APIRouter, Depends
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
import time

router = APIRouter(prefix="/cliente", tags=["Cliente"])

@router.get("/dashboard", summary="Obtener Datos del Cliente", description="Obtener información del dashboard del cliente (perfil, cuentas, tarjetas)")
async def get_client_data(current_user: str = Depends(get_current_user)):
    time.sleep(0.6)
    
    user = MOCK_DATA["users"][current_user]
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    cards = MOCK_DATA["cards"].get(current_user, [])
    
    return {
        "success": True,
        "data": {
            "personalInfo": {
                "name": user["name"],
                "dni": user["dni"],
                "email": user["email"],
                "phone": user["phone"],
                "address": user["address"]
            },
            "accounts": accounts,
            "cards": cards
        }
    }
