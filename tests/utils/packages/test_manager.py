import pytest

from simplexss.utils.packages import PackageManager


@pytest.mark.parametrize(
    "path, name, class_name",
    [
        ("tests/utils/packages/packages/package.py", "hello-package", "Package"),
        ("tests/utils/packages/packages/package_2.py", "hello-package-2", "PackageCls"),
    ],
)
def test_package_loading(path, name, class_name):
    manager = PackageManager()
    package = manager.load_package(path, class_name=class_name)

    assert package.NAME == name


def test_package_unloading():
    manager = PackageManager()
    package = manager.load_package("tests/utils/packages/packages/package.py")

    manager.unload_package(package.NAME)

    assert manager.get_package(package.NAME) is None
    assert len(list(manager.packages)) == 0
