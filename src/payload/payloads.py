from abc import ABC
from typing import Container

from src.package import Package


class BasePayload(Package, ABC):
    TRANSPORT: Container[str]
