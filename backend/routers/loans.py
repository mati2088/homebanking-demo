from fastapi import APIRouter, Depends
from backend.models import SolicitudPrestamo, RespuestaPrestamo
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
from datetime import datetime
import time

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.get("/", summary="Obtener Préstamos", description="Obtener préstamos activos")
async def get_active_loans(current_user: str = Depends(get_current_user)):
    time.sleep(0.5)
    loans = MOCK_DATA["loans"].get(current_user, [])
    return {"exito": True, "prestamos": [l for l in loans if l["status"] == "active"]}

@router.post("/", response_model=RespuestaPrestamo, summary="Solicitar Préstamo", description="Solicitar un préstamo personal")
async def create_loan(request: SolicitudPrestamo, current_user: str = Depends(get_current_user)):
    time.sleep(1.5)
    MAX_LOAN = 500000
    if request.monto > MAX_LOAN:
         return RespuestaPrestamo(exito=False, mensaje=f"Monto máximo ${MAX_LOAN}")
         
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    target_account = next((a for a in accounts if a["id"] == request.cuenta_destino), None)
    
    if not target_account:
        return RespuestaPrestamo(exito=False, mensaje="Cuenta destino inválida")

    # Calculations
    RATE = 0.65
    total_to_pay = request.monto * (1 + (RATE * (request.cuotas / 12)))
    installment_amt = total_to_pay / request.cuotas
    
    target_account["balance"] += request.monto
    
    loan = {
        "id": f"LN{int(time.time())}",
        "amount": request.monto,
        "installments": request.cuotas,
        "installmentAmount": installment_amt,
        "startDate": datetime.now(),
        "status": "active"
    }

    if current_user not in MOCK_DATA["loans"]:
        MOCK_DATA["loans"][current_user] = []
    MOCK_DATA["loans"][current_user].append(loan)

    # Transaction
    txn = {
        "id": f"TXN{int(time.time())}",
        "date": datetime.now(),
        "description": f"Préstamo Personal a {request.cuotas} cuotas",
        "amount": request.monto,
        "type": "credit",
        "account": request.cuenta_destino
    }
    
    if current_user not in MOCK_DATA["transactions"]:
        MOCK_DATA["transactions"][current_user] = []
    MOCK_DATA["transactions"][current_user].insert(0, txn)

    return RespuestaPrestamo(exito=True, mensaje="Préstamo acreditado exitosamente")

@router.delete("/{loan_id}/desistir", response_model=RespuestaPrestamo, summary="Desistir Préstamo", description="Desistir (cancelar) un préstamo dentro de los 10 días")
async def retract_loan(loan_id: str, current_user: str = Depends(get_current_user)):
    time.sleep(1.0)
    loans = MOCK_DATA["loans"].get(current_user, [])
    loan = next((l for l in loans if l["id"] == loan_id), None)
    
    if not loan or loan["status"] != "active":
        return RespuestaPrestamo(exito=False, mensaje="Préstamo no encontrado o no activo")
    
    # Check 10 days
    start_date = loan["startDate"]
    if isinstance(start_date, str):
        pass # Handle if string
        
    days_passed = (datetime.now() - start_date).days
    
    if days_passed > 10:
         return RespuestaPrestamo(exito=False, mensaje=f"No se puede desistir. Han pasado {days_passed} días (límite: 10 días).")
    
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    target_account = accounts[0] 
    
    if target_account["balance"] < loan["amount"]:
         return RespuestaPrestamo(exito=False, mensaje="Saldo insuficiente para devolver el préstamo.")
         
    target_account["balance"] -= loan["amount"]
    loan["status"] = "retracted"
    
    # Transaction
    txn = {
        "id": f"TXN{int(time.time())}",
        "date": datetime.now(),
        "description": f"Desistimiento de Préstamo {loan_id}",
        "amount": -loan["amount"],
        "type": "debit",
        "account": target_account["id"]
    }
    MOCK_DATA["transactions"][current_user].insert(0, txn)
    
    return RespuestaPrestamo(exito=True, mensaje="Préstamo desistido exitosamente")
