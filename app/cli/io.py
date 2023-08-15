from app.io import IOManager
from app.utils import cli


class CLIIOManager(IOManager):
    def print(self, *args):
        print(*args)

    def print_pos(self, *args):
        cli.print_pos(*args)

    def print_neg(self, *args):
        cli.print_neg(*args)

    def print_debug(self, *args):
        if self.debug:
            cli.print_status(*args)

    def ask(self, prompt: str, default: any = None):
        return cli.ask(prompt, default=default)
