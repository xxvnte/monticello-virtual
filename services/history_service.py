import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.history_repository import HistoryRepository
from services.soa_response import build_response, split_payload
from services.soa_service_runner import run_soa_service

SERVICE_NAME = "histo"
repository = HistoryRepository()


def handle_list(parts):
    if len(parts) < 2:
        return build_response(False, "Use: LIST|user_id|limite_opcional")
    user_id = int(parts[1])
    limit = int(parts[2]) if len(parts) > 2 and parts[2] else 20
    if limit < 1 or limit > 100:
        return build_response(False, "El limite debe estar entre 1 y 100")
    items = repository.list_user_history(user_id, limit)
    return build_response(
        True,
        "Historial obtenido",
        {"items": items, "count": len(items)},
    )


def process_payload(payload):
    parts = split_payload(payload)
    if not parts:
        return build_response(False, "Solicitud vacia")
    action = parts[0].upper()
    if action == "LIST":
        return handle_list(parts)
    return build_response(False, "Accion no soportada. Use LIST")


if __name__ == "__main__":
    run_soa_service(SERVICE_NAME, process_payload, "Servicio de historial")
