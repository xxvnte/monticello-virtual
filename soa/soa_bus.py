import socket
import threading

from soa_lib import receive_message, send_message

HOST = "localhost"
PORT = 5000

services = {}
pending_clients = {}
lock = threading.Lock()


def route_to_client(service_name, payload):
    with lock:
        client_sock = pending_clients.pop(service_name, None)
    if client_sock:
        send_message(client_sock, service_name, payload)


def route_to_service(service_name, payload, client_sock):
    with lock:
        service_sock = services.get(service_name)
        if not service_sock:
            send_message(client_sock, service_name, "ERR|servicio no registrado")
            return
        pending_clients[service_name] = client_sock
    send_message(service_sock, service_name, payload)


def handle_connection(conn, addr):
    registered_service = None
    is_service = False
    try:
        while True:
            data = receive_message(conn)
            if not data:
                break
            destination = data[:5].decode(errors="replace")
            body = data[5:].decode(errors="replace")
            if destination == "sinit":
                registered_service = body
                with lock:
                    services[registered_service] = conn
                is_service = True
                send_message(conn, "sinit", "OK")
                print(f"Servicio registrado: {registered_service} ({addr})")
            elif is_service:
                route_to_client(destination, body)
            else:
                route_to_service(destination, body, conn)
    finally:
        with lock:
            if registered_service and services.get(registered_service) == conn:
                services.pop(registered_service, None)
            for name, sock in list(pending_clients.items()):
                if sock == conn:
                    pending_clients.pop(name, None)
        conn.close()
        print(f"Conexión cerrada: {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(50)
    print(f"Bus SOA (ESB) escuchando en {HOST}:{PORT}")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(
                target=handle_connection, args=(conn, addr), daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("Bus SOA detenido.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
