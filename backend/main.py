from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import client, accounts, transactions, transfers, payments, investments, loans, cards, system

tags_metadata = [
    {"name": "Cliente", "description": "Información del perfil y dashboard"},
    {"name": "Cuentas", "description": "Consultas de saldo y cuentas bancarias"},
    {"name": "Transacciones", "description": "Historial de movimientos"},
    {"name": "Transferencias", "description": "Realización de transferencias propias y a terceros"},
    {"name": "Pagos", "description": "Pago de servicios e impuestos"},
    {"name": "Plazos Fijos", "description": "Inversiones y depósitos a plazo"},
    {"name": "Préstamos", "description": "Solicitud y gestión de préstamos personales"},
    {"name": "Tarjetas", "description": "Gestión de tarjetas de crédito, débito y virtuales"},
    {"name": "Sistema", "description": "Utilidades de simulación y reset"}
]

app = FastAPI(
    title="Homebanking Mock API",
    version="1.1.0",
    openapi_tags=tags_metadata
)

# CORS Configuration
origins = [
    "*", # Allow all for local testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# app.include_router(auth.router) # Removed
app.include_router(client.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(transfers.router)
app.include_router(payments.router)
app.include_router(investments.router)
app.include_router(loans.router)
app.include_router(cards.router)
app.include_router(system.router)

@app.get("/")
async def root():
    return {"message": "Homebanking Mock API is running. Visit /docs for Swagger UI."}
