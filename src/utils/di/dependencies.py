class Dependency:
    def __init__(self, base: type, default: any = None):
        self.base = base
        self.default = default

    def __call__(self, default: any):
        self.default = default
        return self

    def __repr__(self):
        return f'<Dependency of {self.base}>'
