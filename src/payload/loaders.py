import os
from abc import ABC, abstractmethod

from src.config import PAYLOAD_CLASS, PAYLOAD_FILE
from src.utils import imputils
from .payloads import BasePayload


class BasePayloadLoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, directory: str) -> BasePayload: ...


class PayloadLoader(BasePayloadLoader):
    @classmethod
    def load(cls, directory: str) -> BasePayload:
        payload_file = os.path.join(directory, PAYLOAD_FILE)
        if not os.path.isfile(payload_file):
            raise ValueError(f'File {PAYLOAD_FILE} not found at {directory}')

        payload_class = imputils.import_class_by_filepath(
            payload_file,
            PAYLOAD_CLASS,
            base_class=BasePayload
        )
        return payload_class()
