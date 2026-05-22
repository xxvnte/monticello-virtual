import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client.soa_invoke import invoke_service, display_response

RULET_SERVICE = "rulet"
WALLE_SERVICE = "walle"
DEFAULT_USER_ID = 1


def print_help():
    print("\nComandos:")
    print("  saldo [user_id]")
    print("  apostar <tipo> <monto>  (rojo, negro, par, impar)")
    print("  apostar numero <n> <monto>")
    print("  ayuda")
    print("  salir")


def parse_bet_command(tokens):
    if len(tokens) < 3:
        raise ValueError("Uso: apostar <tipo> <monto> o apostar numero <n> <monto>")
    bet_type = tokens[0].lower()
    if bet_type == "numero":
        if len(tokens) < 3:
            raise ValueError("Uso: apostar numero <0-36> <monto>")
        return bet_type, tokens[1], float(tokens[2])
    return bet_type, "", float(tokens[1])


def show_spin_result(parsed):
    if parsed.get("balance") is not None:
        print(f"Saldo actual: {parsed['balance']}")
    if parsed.get("winning_number") is not None:
        print(
            f"Numero: {parsed['winning_number']} | Color: {parsed.get('color')} | "
            f"Premio: {parsed.get('prize', 0)}"
        )


def main():
    print_help()
    while True:
        entrada = input("\nRuleta> ").strip()
        if not entrada:
            continue
        if entrada.lower() in {"q", "salir", "exit"}:
            break
        tokens = entrada.split()
        command = tokens[0].lower()
        try:
            if command == "ayuda":
                print_help()
                continue
            if command == "saldo":
                user_id = int(tokens[1]) if len(tokens) > 1 else DEFAULT_USER_ID
                parsed = display_response(
                    invoke_service(WALLE_SERVICE, f"SALDO|{user_id}")
                )
                if parsed and parsed.get("balance") is not None:
                    print(f"Saldo: {parsed['balance']} {parsed.get('currency', 'CLP')}")
                continue
            if command == "apostar":
                bet_type, bet_value, amount = parse_bet_command(tokens[1:])
                payload = f"SPIN|{DEFAULT_USER_ID}|{amount}|{bet_type}|{bet_value}"
                parsed = display_response(invoke_service(RULET_SERVICE, payload))
                if parsed:
                    show_spin_result(parsed)
                continue
            print("Comando no reconocido.")
        except ValueError as error:
            print(f"Entrada invalida: {error}")


if __name__ == "__main__":
    main()
