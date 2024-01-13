class AddressInUseError(Exception):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        super(AddressInUseError, self).__init__(f"Address {host}:{port} already in use. Server can't be launched")


class ServerAlreadyRunningError(Exception):
    def __init__(self):
        super(ServerAlreadyRunningError, self).__init__('Current server is already running')
