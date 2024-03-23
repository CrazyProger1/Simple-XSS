from dataclasses import dataclass


@dataclass
class Session:
    host: str
    port: int
