from simplexss.utils.di import containers, dependencies, inject


def test_inject():
    value = "hello, world!"

    class Container(containers.Container):
        dep = dependencies.Dependency(value)

    @inject
    def clb(dep=Container.dep):
        assert dep == value

    clb()
