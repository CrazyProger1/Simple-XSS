from .enums import Format


class SettingsError(Exception):
    def __init__(self, fmt: Format, file: str, msg: str):
        self.fmt = fmt
        self.file = file
        self.msg = msg
        super(SettingsError, self).__init__(msg)


class FormatError(SettingsError):
    pass


class FileError(SettingsError):
    pass
