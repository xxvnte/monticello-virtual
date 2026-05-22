import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client.soa_invoke import invoke_service, display_response

SERVICE_NAME = "auths"
current_user_id = None


def print_help():
    print("\nComandos:")
    print("  login <correo> <password>")
    print("  registro <rut> <nombre> <apellido> <correo> <password>")
    print("  usuario")
    print("  ayuda")
    print("  salir")


def main():
    global current_user_id
    print_help()
    while True:
        entrada = input("\nAuth> ").strip()
        if not entrada:
            continue
        if entrada.lower() in {"q", "salir", "exit"}:
            break
        tokens = entrada.split()
        command = tokens[0].lower()
        if command == "ayuda":
            print_help()
            continue
        if command == "usuario":
            if current_user_id:
                print(f"Usuario activo: id {current_user_id}")
            else:
                print("No hay sesion. Use login.")
            continue
        if command == "login":
            if len(tokens) < 3:
                print("Uso: login <correo> <password>")
                continue
            payload = f"LOGIN|{tokens[1]}|{tokens[2]}"
            parsed = display_response(invoke_service(SERVICE_NAME, payload))
            if parsed and parsed.get("ok"):
                current_user_id = parsed.get("user_id")
            continue
        if command == "registro":
            if len(tokens) < 6:
                print("Uso: registro <rut> <nombre> <apellido> <correo> <password>")
                continue
            payload = (
                f"REGIST|{tokens[1]}|{tokens[2]}|{tokens[3]}|{tokens[4]}|{tokens[5]}"
            )
            parsed = display_response(invoke_service(SERVICE_NAME, payload))
            if parsed and parsed.get("ok"):
                current_user_id = parsed.get("user_id")
            continue
        print("Comando no reconocido.")


if __name__ == "__main__":
    main()
