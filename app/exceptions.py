class HookLoadingError(ValueError):
    def __init__(self, path: str):
        super().__init__(f'Failed to load hook: {path}')


class PayloadLoadingError(ValueError):
    def __init__(self, path: str):
        super().__init__(f'Failed to load payload: {path}')


class InitFileImportError(ImportError):
    def __init__(self, path: str):
        super().__init__(f'Failed to import payload init file: {path}')
