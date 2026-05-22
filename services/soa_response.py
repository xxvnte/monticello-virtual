import json


def build_response(ok, message, extra=None):
    data = {"ok": ok, "message": message}
    if extra:
        data.update(extra)
    return json.dumps(data, ensure_ascii=False)


def split_payload(payload):
    return [part.strip() for part in payload.split("|")]
