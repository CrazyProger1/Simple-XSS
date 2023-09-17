from app.utils.cli.exceptions import ValidationError


class HookLoadingError(ValueError):
    def __init__(self, path: str):
        super().__init__(f'Failed to load hook: {path}')


class PayloadLoadingError(ValueError):
    def __init__(self, path: str):
        super().__init__(f'Failed to load payload: {path}')


class InitFileImportError(ImportError):
    def __init__(self, path: str):
        super().__init__(f'Failed to import payload init file: {path}')


class HTTPTunnelError(Exception):
    def __init__(self, host: str, port: int):
        super().__init__(f'Failed to open tunnel: {host}:{port}')


class MessageDecodeError(ValueError):
    pass


class MessageEncodeError(ValueError):
    pass
