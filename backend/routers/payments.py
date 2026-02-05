from fastapi import APIRouter, Depends
from backend.models import SolicitudPago, RespuestaPago
from backend.database import MOCK_DATA, CONSTANTS
from backend.dependencies import get_current_user
from datetime import datetime
import time

router = APIRouter(prefix="/pagos", tags=["Pagos"])

@router.post("/servicios", response_model=RespuestaPago, summary="Pagar Servicio", description="Realizar pago de servicios")
async def pay_service(request: SolicitudPago, current_user: str = Depends(get_current_user)):
    time.sleep(1.2)
    
    # 1. Validate Request
    service = next((s for s in CONSTANTS["services"] if s["id"] == request.id_servicio), None)
    if not service:
        return RespuestaPago(exito=False, error="SERVICIO_INVALIDO", mensaje="Servicio no encontrado")
        
    if request.monto <= 0:
        return RespuestaPago(exito=False, error="MONTO_INVALIDO", mensaje="El monto debe ser positivo")

    accounts = MOCK_DATA["accounts"].get(current_user, [])
    account = next((a for a in accounts if a["id"] == request.id_cuenta), None)
    
    if not account:
        return RespuestaPago(exito=False, error="CUENTA_INVALIDA", mensaje="Cuenta inválida")
        
    if account["balance"] < request.monto:
        return RespuestaPago(exito=False, error="FONDOS_INSUFICIENTES", mensaje="Saldo insuficiente")

    # 2. Process Payment
    account["balance"] -= request.monto
    
    # 3. Add Transaction
    txn_id = f"TXN{int(time.time())}"
    transaction = {
        "id": txn_id,
        "date": datetime.now(),
        "description": f"Pago {service['name']} - {service['company']}",
        "amount": -request.monto,
        "type": "debit",
        "account": request.id_cuenta
    }
    
    if current_user not in MOCK_DATA["transactions"]:
        MOCK_DATA["transactions"][current_user] = []
    
    MOCK_DATA["transactions"][current_user].insert(0, transaction)
    
    return RespuestaPago(
        exito=True,
        mensaje=f"Pago de {service['name']} realizado exitosamente",
        comprobante={
            "id": f"REC{int(time.time())}",
            "servicio": service["name"],
            "empresa": service["company"],
            "monto": request.monto,
            "fecha": datetime.now().isoformat(),
            "cuenta": account["displayNumber"]
        }
    )
