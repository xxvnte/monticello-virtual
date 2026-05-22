import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "soa"))

from soa_lib import connect_to_bus, send_message, receive_message


def invoke_service(service_name, payload):
    sock = connect_to_bus()
    try:
        send_message(sock, service_name, payload)
        data = receive_message(sock)
        if not data:
            return None
        return data[5:].decode()
    finally:
        sock.close()


def display_response(raw_response):
    if raw_response is None:
        print("Sin respuesta del bus.")
        return None
    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError:
        print(f"Respuesta: {raw_response}")
        return None
    print(parsed.get("message", raw_response))
    return parsed
