import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client.soa_invoke import invoke_service, display_response

SERVICE_NAME = "walle"
DEFAULT_USER_ID = 1


def print_help():
    print("\nComandos:")
    print("  saldo [user_id]")
    print("  depositar <monto> [user_id]")
    print("  retirar <monto> [user_id]")
    print("  ayuda")
    print("  salir")


def resolve_user_id(tokens, amount_index):
    if len(tokens) > amount_index + 1:
        return int(tokens[amount_index + 1])
    return DEFAULT_USER_ID


def main():
    print_help()
    while True:
        entrada = input("\nBilletera> ").strip()
        if not entrada:
            continue
        if entrada.lower() in {"q", "salir", "exit"}:
            break
        tokens = entrada.split()
        command = tokens[0].lower()
        if command == "ayuda":
            print_help()
            continue
        if command == "saldo":
            user_id = int(tokens[1]) if len(tokens) > 1 else DEFAULT_USER_ID
            parsed = display_response(invoke_service(SERVICE_NAME, f"SALDO|{user_id}"))
            if parsed and parsed.get("balance") is not None:
                print(f"Saldo: {parsed['balance']} {parsed.get('currency', 'CLP')}")
            continue
        if command == "depositar":
            if len(tokens) < 2:
                print("Uso: depositar <monto> [user_id]")
                continue
            user_id = resolve_user_id(tokens, 1)
            amount = tokens[1]
            display_response(invoke_service(SERVICE_NAME, f"DEPOS|{user_id}|{amount}"))
            continue
        if command == "retirar":
            if len(tokens) < 2:
                print("Uso: retirar <monto> [user_id]")
                continue
            user_id = resolve_user_id(tokens, 1)
            amount = tokens[1]
            display_response(invoke_service(SERVICE_NAME, f"RETIR|{user_id}|{amount}"))
            continue
        print("Comando no reconocido.")


if __name__ == "__main__":
    main()
