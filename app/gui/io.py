from app.io import IOManager
from app.utils import observer


class GUIIOManager(IOManager):
    print_event = observer.Event()
    input_event = observer.ResultEvent()
    print_pos_event = observer.Event()
    print_neg_event = observer.Event()
    print_debug_event = observer.Event()

    def print(self, *args):
        self.print_event(args=args)

    def print_debug(self, *args):
        if self.debug:
            self.print_debug_event(args=args)

    def print_pos(self, *args):
        self.print_pos_event(args=args)

    def print_neg(self, *args):
        self.print_neg_event(args=args)

    def input(self, prompt: str):
        return self.input_event(prompt=prompt)
