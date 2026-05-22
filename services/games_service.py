import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.games_repository import GamesRepository
from services.soa_response import build_response, split_payload
from services.soa_service_runner import run_soa_service

SERVICE_NAME = "juego"
repository = GamesRepository()


def serialize_games(rows):
    return [
        {
            "id_juego": row["id_juego"],
            "nombre": row["nombre"],
            "tipo": row["tipo"],
            "descripcion": row["descripcion"],
            "apuesta_min": float(row["apuesta_min"]),
            "apuesta_max": float(row["apuesta_max"]),
        }
        for row in rows
    ]


def handle_list():
    games = repository.list_active_games()
    return build_response(
        True,
        "Catalogo de juegos activos",
        {"games": serialize_games(games), "count": len(games)},
    )


def handle_start(parts):
    if len(parts) < 3:
        return build_response(False, "Use: START|user_id|id_juego")
    user_id = int(parts[1])
    game_id = int(parts[2])
    try:
        game, session = repository.start_session(user_id, game_id)
    except ValueError as error:
        return build_response(False, str(error))
    except Exception as error:
        return build_response(False, f"No se pudo iniciar sesion: {error}")
    return build_response(
        True,
        f"Sesion iniciada en {game['nombre']}",
        {
            "session_id": session["id_sesion"],
            "game_id": game["id_juego"],
            "game_name": game["nombre"],
            "game_type": game["tipo"],
            "started_at": session["inicio"].isoformat(),
        },
    )


def process_payload(payload):
    parts = split_payload(payload)
    if not parts:
        return build_response(False, "Solicitud vacia")
    action = parts[0].upper()
    if action == "LIST":
        return handle_list()
    if action == "START":
        return handle_start(parts)
    return build_response(False, "Accion no soportada. Use LIST o START")


if __name__ == "__main__":
    run_soa_service(SERVICE_NAME, process_payload, "Servicio de juegos")
