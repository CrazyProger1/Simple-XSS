from src.core import payloads


def is_valid_payload_path(path: str) -> bool:
    return payloads.is_payload(path)
