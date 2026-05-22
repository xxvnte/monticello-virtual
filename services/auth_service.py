import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db.auth_repository import AuthRepository
from services.soa_response import build_response, split_payload
from services.soa_service_runner import run_soa_service

SERVICE_NAME = "auths"
repository = AuthRepository()


def handle_login(parts):
    if len(parts) < 3:
        return build_response(False, "Use: LOGIN|correo|password")
    email = parts[1]
    password = parts[2]
    user = repository.login(email, password)
    if not user:
        return build_response(False, "Credenciales invalidas")
    if not user["activo"]:
        return build_response(False, "Cuenta suspendida")
    return build_response(
        True,
        "Autenticacion exitosa",
        {
            "user_id": user["id_usuario"],
            "nombre": user["nombre"],
            "apellido": user["apellido"],
            "correo": user["correo"],
            "rol": user["rol"],
        },
    )


def handle_register(parts):
    if len(parts) < 6:
        return build_response(
            False,
            "Use: REGIST|rut|nombre|apellido|correo|password",
        )
    rut = parts[1]
    nombre = parts[2]
    apellido = parts[3]
    email = parts[4]
    password = parts[5]
    try:
        user, wallet_id = repository.register(rut, nombre, apellido, email, password)
    except Exception as error:
        return build_response(False, f"No se pudo registrar: {error}")
    return build_response(
        True,
        "Registro exitoso",
        {
            "user_id": user["id_usuario"],
            "correo": user["correo"],
            "wallet_id": wallet_id,
        },
    )


def process_payload(payload):
    parts = split_payload(payload)
    if not parts:
        return build_response(False, "Solicitud vacia")
    action = parts[0].upper()
    if action == "LOGIN":
        return handle_login(parts)
    if action == "REGIST":
        return handle_register(parts)
    return build_response(False, "Accion no soportada. Use LOGIN o REGIST")


if __name__ == "__main__":
    run_soa_service(SERVICE_NAME, process_payload, "Servicio de autenticacion")
