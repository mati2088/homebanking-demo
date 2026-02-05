from fastapi import APIRouter, Depends
from backend.models import SolicitudTarjetaVirtual, RespuestaTarjeta
from backend.database import MOCK_DATA
from backend.dependencies import get_current_user
from datetime import datetime
import time
import random

router = APIRouter(prefix="/tarjetas", tags=["Tarjetas"])

@router.get("/virtuales", summary="Obtener Tarjetas Virtuales", description="Obtener tarjetas virtuales activas")
async def get_virtual_cards(current_user: str = Depends(get_current_user)):
    cards = MOCK_DATA["virtualCards"].get(current_user, [])
    return cards

@router.post("/virtuales", response_model=RespuestaTarjeta, summary="Generar Tarjeta Virtual", description="Generar una nueva tarjeta virtual")
async def create_virtual_card(request: SolicitudTarjetaVirtual, current_user: str = Depends(get_current_user)):
    time.sleep(1.5)
    
    # Validate Account Exists
    accounts = MOCK_DATA["accounts"].get(current_user, [])
    account_exists = any(a["id"] == request.id_cuenta_asociada for a in accounts)
    
    if not account_exists:
        return RespuestaTarjeta(exito=False, error="CUENTA_INEXISTENTE", mensaje="La cuenta indicada no existe o no pertenece al usuario.")

    virtual_cards = MOCK_DATA["virtualCards"].get(current_user, [])
    if any(c["linkedAccount"] == request.id_cuenta_asociada for c in virtual_cards):
         return RespuestaTarjeta(exito=False, error="YA_TIENE_TARJETA", mensaje="Esta cuenta ya tiene una tarjeta virtual activa.")
    
    # Generate Mock Card
    card_number = '4' + ''.join([str(random.randint(0,9)) for _ in range(15)])
    
    new_card = {
        "id": f"VCARD{int(time.time())}",
        "number": card_number,
        "displayNumber": "**** **** **** " + card_number[-4:],
        "fullNumber": " ".join([card_number[i:i+4] for i in range(0, len(card_number), 4)]),
        "cvv": str(random.randint(100, 999)),
        "expiryDate": f"{random.randint(1,12):02d}/{str(datetime.now().year + 3)[-2:]}",
        "linkedAccount": request.id_cuenta_asociada,
        "createdDate": datetime.now(),
        "status": "active"
    }
    
    if current_user not in MOCK_DATA["virtualCards"]:
        MOCK_DATA["virtualCards"][current_user] = []
    MOCK_DATA["virtualCards"][current_user].append(new_card)
    
    return RespuestaTarjeta(exito=True, mensaje="Tarjeta virtual generada exitosamente", tarjeta=new_card)

@router.delete("/virtuales/{card_id}", summary="Eliminar Tarjeta Virtual", description="Eliminar una tarjeta virtual")
async def delete_virtual_card(card_id: str, current_user: str = Depends(get_current_user)):
    time.sleep(0.8)
    virtual_cards = MOCK_DATA["virtualCards"].get(current_user, [])
    
    initial_len = len(virtual_cards)
    virtual_cards[:] = [c for c in virtual_cards if c["id"] != card_id]
    
    if len(virtual_cards) == initial_len:
        return {"exito": False, "mensaje": "Tarjeta no encontrada"}
        
    return {"exito": True, "mensaje": "Tarjeta eliminada exitosamente"}
