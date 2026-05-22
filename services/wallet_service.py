import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.wallet_repository import WalletRepository
from services.soa_response import build_response, split_payload
from services.soa_service_runner import run_soa_service

SERVICE_NAME = "walle"
repository = WalletRepository()


def parse_user_id(parts, index=1):
    return int(parts[index])


def handle_balance(parts):
    if len(parts) < 2:
        return build_response(False, "Use: SALDO|user_id")
    user_id = parse_user_id(parts)
    wallet = repository.get_wallet(user_id)
    if not wallet or not wallet["activo"]:
        return build_response(False, "Billetera no encontrada")
    return build_response(
        True,
        "Saldo consultado",
        {"balance": float(wallet["saldo"]), "currency": wallet["moneda"]},
    )


def handle_movement(parts, movement_type):
    if len(parts) < 3:
        label = "DEPOS" if movement_type == "deposito" else "RETIR"
        return build_response(False, f"Use: {label}|user_id|monto")
    user_id = parse_user_id(parts)
    amount = float(parts[2])
    try:
        result = repository.apply_movement(user_id, movement_type, amount)
    except ValueError as error:
        return build_response(False, str(error))
    except Exception as error:
        return build_response(False, f"Error en movimiento: {error}")
    verb = "depositado" if movement_type == "deposito" else "retirado"
    return build_response(
        True,
        f"Monto {verb} correctamente",
        {
            "balance": result["balance"],
            "currency": result["currency"],
            "transaction_type": result["transaction_type"],
        },
    )


def process_payload(payload):
    parts = split_payload(payload)
    if not parts:
        return build_response(False, "Solicitud vacia")
    action = parts[0].upper()
    if action == "SALDO":
        return handle_balance(parts)
    if action == "DEPOS":
        return handle_movement(parts, "deposito")
    if action == "RETIR":
        return handle_movement(parts, "retiro")
    return build_response(False, "Accion no soportada. Use SALDO, DEPOS o RETIR")


if __name__ == "__main__":
    run_soa_service(SERVICE_NAME, process_payload, "Servicio de billetera")
