
from datetime import datetime, timedelta

# Helper to create dates relative to now
def days_ago(days):
    return datetime.now() - timedelta(days=days)

def days_future(days):
    return datetime.now() + timedelta(days=days)

MOCK_DATA = {
    "users": {
        "demo": {
            "username": "demo",
            "password": "demo123",
            "name": "Juan Pérez",
            "dni": "12.345.678",
            "email": "juan.perez@email.com",
            "phone": "+54 11 1234-5678",
            "address": "Av. Corrientes 1234, CABA, Argentina",
            "locked": False
        },
        "wrong": {
            "username": "wrong",
            "password": "correct123",
            "name": "Usuario Test",
            "locked": False
        },
        "locked": {
            "username": "locked",
            "password": "locked",
            "name": "Usuario Bloqueado",
            "locked": True
        }
    },
    "accounts": {
        "demo": [
            {
                "id": "ACC001",
                "type": "Cuenta Corriente",
                "number": "1234567890123456",
                "displayNumber": "**** **** **** 1234",
                "balance": 125450.75,
                "currency": "ARS",
                "cbu": "0170001234567890123456"
            },
            {
                "id": "ACC002",
                "type": "Caja de Ahorro",
                "number": "5678901234567890",
                "displayNumber": "**** **** **** 5678",
                "balance": 89320.50,
                "currency": "ARS",
                "cbu": "0170005678901234567890"
            },
            {
                "id": "ACC003",
                "type": "Tarjeta de Crédito",
                "number": "9012345678901234",
                "displayNumber": "**** **** **** 9012",
                "balance": 45000.00,
                "limit": 150000.00,
                "currency": "ARS"
            }
        ]
    },
    "transactions": {
        "demo": [
            {
                "id": "TXN001",
                "date": days_ago(1),
                "description": "Transferencia recibida",
                "amount": 15000.00,
                "type": "credit",
                "account": "ACC001"
            },
            {
                "id": "TXN002",
                "date": days_ago(2),
                "description": "Pago de servicios",
                "amount": -3250.50,
                "type": "debit",
                "account": "ACC001"
            },
            {
                "id": "TXN003",
                "date": days_ago(3),
                "description": "Compra en supermercado",
                "amount": -8450.25,
                "type": "debit",
                "account": "ACC003"
            },
            {
                "id": "TXN004",
                "date": days_ago(4),
                "description": "Depósito en efectivo",
                "amount": 25000.00,
                "type": "credit",
                "account": "ACC002"
            },
            {
                "id": "TXN005",
                "date": days_ago(5),
                "description": "Transferencia enviada",
                "amount": -12000.00,
                "type": "debit",
                "account": "ACC001"
            },
            {
                "id": "TXN006",
                "date": days_ago(6),
                "description": "Pago de tarjeta",
                "amount": -5000.00,
                "type": "debit",
                "account": "ACC002"
            },
            {
                "id": "TXN007",
                "date": days_ago(7),
                "description": "Compra online",
                "amount": -2850.00,
                "type": "debit",
                "account": "ACC003"
            },
            {
                "id": "TXN008",
                "date": days_ago(8),
                "description": "Transferencia recibida",
                "amount": 8500.00,
                "type": "credit",
                "account": "ACC001"
            },
            {
                "id": "TXN009",
                "date": days_ago(9),
                "description": "Retiro cajero automático",
                "amount": -5000.00,
                "type": "debit",
                "account": "ACC001"
            },
            {
                "id": "TXN010",
                "date": days_ago(10),
                "description": "Sueldo",
                "amount": 95000.00,
                "type": "credit",
                "account": "ACC001"
            }
        ]
    },
    "fixedDeposits": {
        "demo": [
            {
                "id": "FD001",
                "amount": 50000.00,
                "term": 90,
                "rate": 42,
                "startDate": days_ago(30),
                "maturityDate": days_future(60),
                "estimatedInterest": 5178.08,
                "status": "active"
            },
            {
                "id": "FD002",
                "amount": 30000.00,
                "term": 60,
                "rate": 38,
                "startDate": days_ago(15),
                "maturityDate": days_future(45),
                "estimatedInterest": 1876.71,
                "status": "active"
            }
        ]
    },
    "loans": {
        "demo": [
            {
                "id": "LN001",
                "amount": 150000.00,
                "installments": 12,
                "installmentAmount": 17500.00,
                "startDate": days_ago(30),
                "status": "active"
            }
        ]
    },
    "cards": {
        "demo": [
            {
                "id": "CARD001",
                "type": "Débito",
                "number": "1234567890123456",
                "displayNumber": "**** **** **** 1234",
                "brand": "Visa",
                "expiryDate": "12/26",
                "linkedAccount": "ACC001"
            },
            {
                "id": "CARD002",
                "type": "Débito",
                "number": "5678901234567890",
                "displayNumber": "**** **** **** 5678",
                "brand": "Mastercard",
                "expiryDate": "08/27",
                "linkedAccount": "ACC002"
            },
            {
                "id": "CARD003",
                "type": "Crédito",
                "number": "9012345678901234",
                "displayNumber": "**** **** **** 9012",
                "brand": "Visa",
                "expiryDate": "03/28",
                "limit": 150000.00,
                "available": 45000.00
            }
        ]
    },
    "beneficiaries": {
        "demo": [
            {
                "id": "BEN001",
                "name": "María González",
                "cbu": "0170009876543210987654",
                "alias": "MARIA.GONZALEZ.MP"
            },
            {
                "id": "BEN002",
                "name": "Carlos Rodríguez",
                "cbu": "0340001122334455667788",
                "alias": "CARLOS.ROD.BANCO"
            }
        ]
    },
    "virtualCards": {
        "demo": []
    }
}

CONSTANTS = {
    "interestRates": {
        30: 35,
        60: 38,
        90: 42,
        180: 45,
        360: 50
    },
    "transferLimits": {
        "dailyLimit": 100000.00,
        "perTransferLimit": 50000.00,
        "minimumAmount": 1.00
    },
    "depositLimits": {
        "minimumAmount": 1000.00,
        "maximumActive": 5
    },
    "services": [
        { "id": "SRV001", "name": "Electricidad", "icon": "⚡", "suggestedAmount": 8500.00, "company": "Edenor", "cuit": "30-11223344-5" },
        { "id": "SRV002", "name": "Gas Natural", "icon": "🔥", "suggestedAmount": 4200.00, "company": "MetroGAS", "cuit": "30-55667788-9" },
        { "id": "SRV003", "name": "Agua", "icon": "💧", "suggestedAmount": 2800.00, "company": "AySA", "cuit": "33-99887766-4" },
        { "id": "SRV004", "name": "Internet", "icon": "🌐", "suggestedAmount": 12000.00, "company": "Fibertel", "cuit": "30-44332211-8" },
        { "id": "SRV005", "name": "Telefonía", "icon": "📱", "suggestedAmount": 6500.00, "company": "Personal", "cuit": "30-66554433-2" }
    ]
}
