from fastapi import APIRouter, Depends
from backend.models import SolicitudTransferencia, RespuestaTransferencia
from backend.database import MOCK_DATA, CONSTANTS
from backend.dependencies import get_current_user
from datetime import datetime
import time

router = APIRouter(prefix="/transferencias", tags=["Transferencias"])

# In-memory daily tracker
daily_transferred = 0

@router.post("/", response_model=RespuestaTransferencia, summary="Realizar Transferencia", description="Realizar una nueva transferencia")
async def transfer(request: SolicitudTransferencia, current_user: str = Depends(get_current_user)):
    global daily_transferred
    time.sleep(1.2)
    
    try:
        limits = CONSTANTS["transferLimits"]
        
        # 1. Validate Amount
        if request.monto < limits["minimumAmount"]:
            return RespuestaTransferencia(exito=False, error="MONTO_INVALIDO", mensaje=f"El monto mínimo es ${limits['minimumAmount']}")
            
        if request.monto > limits["perTransferLimit"]:
            return RespuestaTransferencia(exito=False, error="LIMITE_EXCEDIDO", mensaje=f"Monto máximo por transferencia superado")

        if daily_transferred + request.monto > limits["dailyLimit"]:
            return RespuestaTransferencia(exito=False, error="LIMITE_DIARIO_EXCEDIDO", mensaje="Límite diario excedido")

        # 2. Get Source Account
        accounts = MOCK_DATA["accounts"].get(current_user, [])
        source_account = next((a for a in accounts if a["id"] == request.cuenta_origen), None)
        
        if not source_account:
            return RespuestaTransferencia(exito=False, error="CUENTA_INVALIDA", mensaje="Cuenta origen no válida")

        if source_account["balance"] < request.monto:
            return RespuestaTransferencia(exito=False, error="FONDOS_INSUFICIENTES", mensaje="Saldo insuficiente")

        # 3. Validate Destination (Mock Logic)
        if request.tipo == 'terceros':
            if len(request.cuenta_destino) < 10:
                 return RespuestaTransferencia(exito=False, error="DESTINO_INVALIDO", mensaje="CBU/Alias inválido")
            if request.cuenta_destino == '0000000000000000000000':
                 return RespuestaTransferencia(exito=False, error="DESTINO_INVALIDO", mensaje="Cuenta destino inexistente")

        # 4. Execute Transfer
        source_account["balance"] -= request.monto
        daily_transferred += request.monto
        
        # 5. Create Transaction Record
        txn_id = f"TXN{int(time.time())}"
        Transaction = {
            "id": txn_id,
            "date": datetime.now(),
            "description": request.motivo or ("Transferencia terceros" if request.tipo == "terceros" else "Transferencia propia"),
            "amount": -request.monto,
            "type": "debit",
            "account": request.cuenta_origen
        }
        
        if current_user not in MOCK_DATA["transactions"]:
            MOCK_DATA["transactions"][current_user] = []
        
        MOCK_DATA["transactions"][current_user].insert(0, Transaction)
        
        # Handle 'own' transfer credit
        if request.tipo == 'propia':
            dest_account = next((a for a in accounts if a["id"] == request.cuenta_destino), None)
            if dest_account:
                dest_account["balance"] += request.monto
                # Credit Transaction
                credit_txn = {
                    "id": f"TXN{int(time.time())+1}",
                    "date": datetime.now(),
                    "description": "Transferencia entre cuentas propias",
                    "amount": request.monto,
                    "type": "credit",
                    "account": request.cuenta_destino
                }
                MOCK_DATA["transactions"][current_user].insert(0, credit_txn)

        return RespuestaTransferencia(
            exito=True,
            transaccion={
                "id": txn_id,
                "fecha": Transaction["date"].isoformat(),
                "monto": request.monto,
                "cuenta_origen": source_account["displayNumber"],
                "cuenta_destino": request.cuenta_destino, 
                "descripcion": Transaction["description"]
            },
            mensaje="Transferencia realizada exitosamente"
        )
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        with open("debug_error.txt", "w") as f:
            f.write(error_msg)
        return RespuestaTransferencia(exito=False, error="SERVER_ERROR", mensaje=f"Error interno: {str(e)}")
