from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

# --- Transfer Models ---
class SolicitudTransferencia(BaseModel):
    cuenta_origen: str = Field(..., description="ID de la cuenta de origen", example="ACC001")
    cuenta_destino: str = Field(..., description="CBU, Alias o ID de la cuenta destino", example="ACC002")
    monto: float = Field(..., description="Monto a transferir", gt=0, example=1500.00)
    motivo: Optional[str] = Field(None, description="Motivo o descripción de la transferencia", example="Alquiler")
    tipo: str = Field(..., description="Tipo de transferencia: 'propia' o 'terceros'", example="propia")

    class Config:
        json_schema_extra = {
            "example": {
                "cuenta_origen": "ACC001",
                "cuenta_destino": "ACC002",
                "monto": 1500.00,
                "motivo": "Varios",
                "tipo": "propia"
            }
        }

class RespuestaTransferencia(BaseModel):
    exito: bool
    transaccion: Optional[dict] = None
    error: Optional[str] = None
    mensaje: str

# --- Fixed Deposit Models ---
class SolicitudPlazoFijo(BaseModel):
    cuenta_origen: str = Field(..., description="ID de la cuenta de origen", example="ACC001")
    monto: float = Field(..., description="Monto a invertir", gt=0, example=50000.00)
    plazo_dias: int = Field(..., description="Plazo en días (30, 60, 90, 180, 360)", example=30)

    class Config:
        json_schema_extra = {
            "example": {
                "cuenta_origen": "ACC001",
                "monto": 50000.00,
                "plazo_dias": 30
            }
        }

class RespuestaPlazoFijo(BaseModel):
    exito: bool
    plazo_fijo: Optional[dict] = None
    error: Optional[str] = None
    mensaje: str

# --- Loan Models ---
class SolicitudPrestamo(BaseModel):
    monto: float = Field(..., description="Monto del préstamo solicitado", gt=0, example=200000.00)
    cuotas: int = Field(..., description="Cantidad de cuotas (6, 12, 24, etc.)", example=12)
    cuenta_destino: str = Field(..., description="ID de la cuenta donde se acreditará", example="ACC001")

    class Config:
        json_schema_extra = {
            "example": {
                "monto": 200000.00,
                "cuotas": 12,
                "cuenta_destino": "ACC001"
            }
        }

class RespuestaPrestamo(BaseModel):
    exito: bool
    mensaje: str
    error: Optional[str] = None

# --- Payment Models ---
class SolicitudPago(BaseModel):
    id_servicio: str = Field(..., description="ID del servicio a pagar", example="SRV001")
    monto: float = Field(..., description="Monto a pagar", gt=0, example=8500.00)
    id_cuenta: str = Field(..., description="ID de la cuenta de débito", example="ACC001")

    class Config:
        json_schema_extra = {
            "example": {
                "id_servicio": "SRV001",
                "monto": 8500.00,
                "id_cuenta": "ACC001"
            }
        }

class RespuestaPago(BaseModel):
    exito: bool
    mensaje: str
    comprobante: Optional[dict] = None
    error: Optional[str] = None

# --- Card Models ---
class SolicitudTarjetaVirtual(BaseModel):
    id_cuenta_asociada: str = Field(..., description="ID de la cuenta asociada a la tarjeta", example="ACC001")

    class Config:
        json_schema_extra = {
            "example": {
                "id_cuenta_asociada": "ACC001"
            }
        }

class RespuestaTarjeta(BaseModel):
    exito: bool
    mensaje: str
    tarjeta: Optional[dict] = None
    error: Optional[str] = None
