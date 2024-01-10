from dataclasses import dataclass

from src.core.enums import Protocol


@dataclass
class Session:
    protocol: str | Protocol
    port: int
    public_url: str

