import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.roulette_repository import RouletteRepository
from services.roulette_engine import spin_wheel, validate_bet, evaluate_bet
from services.soa_response import build_response, split_payload
from services.soa_service_runner import run_soa_service

SERVICE_NAME = "rulet"
repository = RouletteRepository()


def handle_spin(parts):
    if len(parts) < 5:
        return build_response(False, "Use: SPIN|user_id|monto|tipo|valor")
    user_id = int(parts[1])
    amount = float(parts[2])
    bet_type = parts[3].lower()
    bet_value = parts[4] if len(parts) > 4 else ""
    wallet = repository.get_user_wallet(user_id)
    if not wallet or not wallet["activo"]:
        return build_response(False, "Usuario no encontrado o inactivo")
    game = repository.get_ruleta_game()
    if not game:
        return build_response(False, "Juego de ruleta no disponible")
    validation_error = validate_bet(
        bet_type,
        bet_value,
        amount,
        float(game["apuesta_min"]),
        float(game["apuesta_max"]),
    )
    if validation_error:
        return build_response(False, validation_error)
    if float(wallet["saldo"]) < amount:
        return build_response(False, "Saldo insuficiente")
    winning_number = spin_wheel()
    won, prize, color = evaluate_bet(winning_number, bet_type, bet_value, amount)
    spin_detail = {
        "winning_number": winning_number,
        "color": color,
        "bet_type": bet_type,
        "bet_value": bet_value,
    }
    result = repository.process_spin(user_id, amount, won, prize, spin_detail)
    outcome = "ganaste" if won else "perdiste"
    return build_response(
        True,
        f"Numero {winning_number} ({color}). {outcome}.",
        {
            "winning_number": winning_number,
            "color": color,
            "won": won,
            "prize": prize,
            "balance": result["balance"],
            "bet_id": result["bet_id"],
            "session_id": result["session_id"],
        },
    )


def process_payload(payload):
    parts = split_payload(payload)
    if not parts:
        return build_response(False, "Solicitud vacia")
    action = parts[0].upper()
    if action == "SPIN":
        return handle_spin(parts)
    return build_response(
        False,
        "Accion no soportada. Use SPIN (saldo via servicio walle)",
    )


if __name__ == "__main__":
    run_soa_service(SERVICE_NAME, process_payload, "Servicio de apuestas (ruleta)")
