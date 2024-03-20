from simplexss.utils.packages import (
    PackageManager,
)


def test_package_loading():
    manager = PackageManager()
    package = manager.load_package(
        'tests/utils/packages/plugin.py',
    )

    assert package.NAME == 'hello-package'
