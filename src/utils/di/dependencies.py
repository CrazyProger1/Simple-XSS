class Dependency:
    def __init__(self, base: type):
        self.base = base

    def __repr__(self):
        return f'<Dependency of {self.base}>'
