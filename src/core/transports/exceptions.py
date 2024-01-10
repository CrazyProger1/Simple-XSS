from .events import address_in_use_error_occurred


class AddressInUseError(Exception):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        address_in_use_error_occurred()
        super(AddressInUseError, self).__init__(f"Address {host}:{port} already in use. Server can't be launched")
