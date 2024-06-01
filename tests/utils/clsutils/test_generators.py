import pytest

from simplexss.utils.clsutils import iter_instances, iter_subclasses


class FirstClass:
    pass


class FirstSubclass(FirstClass):
    pass


class FirstSubSubClass(FirstSubclass):
    pass


@pytest.fixture
def create_instances():
    return [
        FirstClass(),
        FirstClass(),
        FirstClass(),
        FirstSubclass(),
        FirstSubSubClass(),
    ]


def test_iter_instances_precise(create_instances):
    instances = tuple(iter_instances(FirstClass, precise=True))

    assert len(instances) == 3


def test_iter_instances_not_precise(create_instances):
    instances = tuple(iter_instances(FirstClass, precise=False))

    assert len(instances) == 5


def test_iter_subclasses_max_level_1():
    subclasses = tuple(iter_subclasses(FirstClass, max_level=1))

    assert len(subclasses) == 1
    assert subclasses[0] == FirstSubclass


def test_iter_subclasses_max_level_neg_1():
    subclasses = tuple(iter_subclasses(FirstClass, max_level=-1))

    assert len(subclasses) == 2


def test_iter_subclasses_max_level_0():
    subclasses = tuple(iter_subclasses(FirstClass, max_level=0))

    assert len(subclasses) == 0
