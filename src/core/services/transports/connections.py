from abc import ABC


class Connection(ABC):
    def send(self, event):
        pass
