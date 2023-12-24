from dataclasses import dataclass

from .enums import Protocol


@dataclass
class Session:
    protocol: str | Protocol
    port: int
    public_url: str

