import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from client.soa_invoke import invoke_service, display_response

SERVICE_NAME = "juego"
DEFAULT_USER_ID = 1


def print_help():
    print("\nComandos:")
    print("  listar")
    print("  iniciar <id_juego> [user_id]")
    print("  ayuda")
    print("  salir")


def main():
    print_help()
    while True:
        entrada = input("\nJuegos> ").strip()
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
            parsed = display_response(invoke_service(SERVICE_NAME, "LIST"))
            if parsed and parsed.get("games"):
                for game in parsed["games"]:
                    print(
                        f"  [{game['id_juego']}] {game['nombre']} ({game['tipo']}) "
                        f"${game['apuesta_min']}-${game['apuesta_max']}"
                    )
            continue
        if command == "iniciar":
            if len(tokens) < 2:
                print("Uso: iniciar <id_juego> [user_id]")
                continue
            game_id = tokens[1]
            try:
                game_id_int = int(game_id)
            except ValueError:
                print("Uso: iniciar <id_juego> [user_id]  (id numerico del catalogo, ej. iniciar 1)")
                continue
            user_id = tokens[2] if len(tokens) > 2 else DEFAULT_USER_ID
            parsed = display_response(
                invoke_service(SERVICE_NAME, f"START|{user_id}|{game_id_int}")
            )
            if parsed and parsed.get("session_id") is not None:
                print(f"ID sesion: {parsed['session_id']}")
            continue
        print("Comando no reconocido.")


if __name__ == "__main__":
    main()
