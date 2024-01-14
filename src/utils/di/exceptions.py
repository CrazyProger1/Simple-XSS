class DIError(Exception):
    pass


class DependencyNotBoundError(DIError):
    def __init__(self, dependency):
        self.dependency = dependency
        super(DependencyNotBoundError, self).__init__(
            f'Dependency {self.dependency.container}.{self.dependency.name} not bound')
