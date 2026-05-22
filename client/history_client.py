import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client.soa_invoke import invoke_service, display_response

SERVICE_NAME = "histo"
DEFAULT_USER_ID = 1


def print_help():
    print("\nComandos:")
    print("  listar [user_id] [limite]")
    print("  ayuda")
    print("  salir")


def main():
    print_help()
    while True:
        entrada = input("\nHistorial> ").strip()
        if not entrada:
            continue
        if entrada.lower() in {"q", "salir", "exit"}:
            break
        tokens = entrada.split()
        command = tokens[0].lower()
        if command == "ayuda":
            print_help()
            continue
        if command == "listar":
            user_id = tokens[1] if len(tokens) > 1 else str(DEFAULT_USER_ID)
            limit = tokens[2] if len(tokens) > 2 else "20"
            parsed = display_response(
                invoke_service(SERVICE_NAME, f"LIST|{user_id}|{limit}")
            )
            if parsed and parsed.get("items"):
                for item in parsed["items"]:
                    print(
                        f"  #{item['id_transaccion']} {item['tipo']} "
                        f"${item['monto']} -> saldo {item['saldo_posterior']} "
                        f"({item['timestamp']})"
                    )
            continue
        print("Comando no reconocido.")


if __name__ == "__main__":
    main()
