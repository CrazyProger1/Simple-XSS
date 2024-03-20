class PackageError(Exception):
    msg = 'Package error: {package}'

    def __init__(self, package: str, msg: str = None):
        self.package = package
        self.msg = msg or self.msg
        super().__init__(self.msg.format(package=package))


class PackageNotFoundError(PackageError):
    msg = 'Package not found: {package}'


class PackageFormatError(PackageError):
    msg = "Package {package} has wrong format, so it can't be loaded"


class PackageDisabledError(PackageError):
    msg = 'Package is disabled: {package}'


class PackageNotLoadedError(PackageError):
    msg = 'Package is not loaded: {package}'
