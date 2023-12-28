from abc import ABC
from typing import Container

from src.utils import packages


class BasePayload(packages.BasePackage, ABC):
    TRANSPORT: Container[str]
