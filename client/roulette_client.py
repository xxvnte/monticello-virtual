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
    print("  apostar <tipo> <monto> [user_id]  (rojo, negro, par, impar)")
    print("  apostar numero <n> <monto> [user_id]")
    print("  ayuda")
    print("  salir")
    print(f"  (sin user_id se usa {DEFAULT_USER_ID}, usuario demo tras init_database)")


def resolve_user_id(tokens, amount_index):
    if len(tokens) > amount_index + 1:
        return int(tokens[amount_index + 1])
    return DEFAULT_USER_ID


def parse_bet_command(tokens):
    if not tokens:
        raise ValueError(
            "Uso: apostar <tipo> <monto> [user_id] o apostar numero <n> <monto> [user_id]"
        )
    bet_type = tokens[0].lower()
    if bet_type == "numero":
        if len(tokens) < 3:
            raise ValueError("Uso: apostar numero <0-36> <monto> [user_id]")
        amount_index = 2
        bet_value = tokens[1]
        amount = float(tokens[2])
    else:
        if len(tokens) < 2:
            raise ValueError(
                "Uso: apostar <tipo> <monto> [user_id] o apostar numero <n> <monto> [user_id]"
            )
        amount_index = 1
        bet_value = ""
        amount = float(tokens[1])
    user_id = resolve_user_id(tokens, amount_index)
    return bet_type, bet_value, amount, user_id


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
                bet_type, bet_value, amount, user_id = parse_bet_command(tokens[1:])
                payload = f"SPIN|{user_id}|{amount}|{bet_type}|{bet_value}"
                parsed = display_response(invoke_service(RULET_SERVICE, payload))
                if parsed:
                    show_spin_result(parsed)
                continue
            print("Comando no reconocido.")
        except ValueError as error:
            print(f"Entrada invalida: {error}")


if __name__ == "__main__":
    main()
