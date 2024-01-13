import json

from fastapi import Request


def get_fingerprint(request: Request) -> int:
    return hash(json.dumps({
        "user_agent": request.headers.get('user-agent'),
        "accept_language": request.headers.get("accept-language"),
        "remote_address": request.client.host,
    }))
