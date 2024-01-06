from src.core.enums import Protocol


class TunnelingError(Exception):
    pass


class TunnelError(TunnelingError):
    def __init__(self, port: int, msg: str):
        self.port = port
        super(TunnelError, self).__init__(msg)


class TunnelOpeningError(TunnelError):
    def __init__(self, port: int):
        super(TunnelOpeningError, self).__init__(
            port=port,
            msg=f'Failed to open tunnel for localhost:{port}'
        )


class ProtocolNotSupportedError(TunnelingError):
    def __init__(self, protocol: str | Protocol):
        super(ProtocolNotSupportedError, self).__init__(
            f'Protocol {protocol} is not supported'
        )
