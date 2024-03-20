from dataclasses import dataclass


@dataclass
class Session:
    protocol: str
    port: int
    public_url: str
