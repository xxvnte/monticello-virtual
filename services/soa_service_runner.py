from soa_lib import connect_to_bus, send_message, receive_message


def run_soa_service(service_name, process_payload, ready_label):
    sock = connect_to_bus()
    try:
        print(f"Registrando servicio '{service_name}' en el bus...")
        send_message(sock, "sinit", service_name)
        init_data = receive_message(sock)
        print(f"Confirmacion del bus: {init_data!r}")
        print(f"{ready_label} listo.\n")
        while True:
            data = receive_message(sock)
            if not data:
                print("Conexion cerrada por el bus.")
                break
            request_payload = data[5:].decode()
            print(f"Solicitud recibida: {request_payload}")
            response_payload = process_payload(request_payload)
            send_message(sock, service_name, response_payload)
            print(f"Respuesta enviada: {response_payload}")
    except Exception as error:
        print(f"Error en {ready_label}: {error}")
    finally:
        print(f"Cerrando socket de {service_name}")
        sock.close()
