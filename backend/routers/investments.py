from fastapi import APIRouter, Depends
from backend.models import SolicitudPlazoFijo, RespuestaPlazoFijo
from backend.database import MOCK_DATA, CONSTANTS
from backend.dependencies import get_current_user
from datetime import datetime, timedelta
import time

router = APIRouter(prefix="/plazos-fijos", tags=["Plazos Fijos"])

@router.post("/", response_model=RespuestaPlazoFijo, summary="Crear Plazo Fijo", description="Crear un nuevo plazo fijo")
async def create_deposit(request: SolicitudPlazoFijo, current_user: str = Depends(get_current_user)):
    time.sleep(1.0)
    
    limits = CONSTANTS["depositLimits"]
    
    # Validation
    if request.monto < limits["minimumAmount"]:
        return RespuestaPlazoFijo(exito=False, error="MONTO_MINIMO", mensaje=f"Monto mínimo ${limits['minimumAmount']}")

    active_deposits = [d for d in MOCK_DATA["fixedDeposits"].get(current_user, []) if d["status"] == "active"]
    if len(active_deposits) >= limits["maximumActive"]:
        return RespuestaPlazoFijo(exito=False, error="MAXIMO_ALCANZADO", mensaje=f"Máximo {limits['maximumActive']} plazos fijos activos")

    accounts = MOCK_DATA["accounts"].get(current_user, [])
    account = next((a for a in accounts if a["id"] == request.cuenta_origen), None)
    
    if not account or account["balance"] < request.monto:
        return RespuestaPlazoFijo(exito=False, error="FONDOS_INSUFICIENTES", mensaje="Saldo insuficiente")

    # Create Deposit
    rate = CONSTANTS["interestRates"].get(request.plazo_dias, 30) 
    interest = (request.monto * rate * request.plazo_dias) / (365 * 100)
    
    deposit = {
        "id": f"FD{int(time.time())}",
        "amount": request.monto,
        "term": request.plazo_dias,
        "rate": rate,
        "startDate": datetime.now(),
        "maturityDate": datetime.now() + timedelta(days=request.plazo_dias),
        "estimatedInterest": interest,
        "status": "active"
    }
    
    account["balance"] -= request.monto
    
    if current_user not in MOCK_DATA["fixedDeposits"]:
        MOCK_DATA["fixedDeposits"][current_user] = []
    MOCK_DATA["fixedDeposits"][current_user].append(deposit)
    
    # Transaction
    txn = {
        "id": f"TXN{int(time.time())}",
        "date": datetime.now(),
        "description": f"Plazo fijo {request.plazo_dias} días",
        "amount": -request.monto,
        "type": "debit",
        "account": request.cuenta_origen
    }
     
    if current_user not in MOCK_DATA["transactions"]:
        MOCK_DATA["transactions"][current_user] = []
    MOCK_DATA["transactions"][current_user].insert(0, txn)

    return RespuestaPlazoFijo(exito=True, plazo_fijo=deposit, mensaje="Plazo fijo creado exitosamente")

@router.get("/", summary="Listar Plazos Fijos", description="Obtener plazos fijos activos")
async def get_active_deposits(current_user: str = Depends(get_current_user)):
    time.sleep(0.5)
    deposits = MOCK_DATA["fixedDeposits"].get(current_user, [])
    return {"exito": True, "plazos_fijos": [d for d in deposits if d["status"] == "active"]}

@router.delete("/{id}", summary="Cancelar Plazo Fijo", description="Cancelar un plazo fijo")
async def cancel_deposit(id: str, current_user: str = Depends(get_current_user)):
    time.sleep(0.8)
    deposits = MOCK_DATA["fixedDeposits"].get(current_user, [])
    deposit = next((d for d in deposits if d["id"] == id), None)
    
    if not deposit or deposit["status"] != "active":
        return {"exito": False, "mensaje": "Plazo fijo no válido o no activo"}

    # Refund
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    target_account = accounts[0] 
    
    target_account["balance"] += deposit["amount"]
    deposit["status"] = "cancelled"
    
    # Transaction
    txn = {
         "id": f"TXN{int(time.time())}",
        "date": datetime.now(),
        "description": f"Cancelación Plazo Fijo {deposit['term']} días",
        "amount": deposit["amount"],
        "type": "credit",
        "account": target_account["id"]
    }
    
    if current_user not in MOCK_DATA["transactions"]:
        MOCK_DATA["transactions"][current_user] = []
    MOCK_DATA["transactions"][current_user].insert(0, txn)

    return {"exito": True, "mensaje": "Plazo fijo cancelado exitosamente"}
