from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def run(self): ...
