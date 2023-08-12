from app.io import IOManager


class CLIIOManager(IOManager):
    def print(self, *args):
        print(*args)

    def input(self, prompt: str):
        return input(prompt)
