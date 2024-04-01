class SettingsError(Exception):
    pass


class FileFormatError(SettingsError):
    def __init__(self, file: str, msg: str):
        self.file = file
        super().__init__(msg)
