from app.io import IOManager
from app.utils import observer


class GUIIOManager(IOManager):
    printed = observer.Event()
    wait_input = observer.ResultEvent()

    def print(self, *args):
        self.printed(args=args)

    def input(self, prompt: str):
        return self.wait_input(prompt=prompt)
