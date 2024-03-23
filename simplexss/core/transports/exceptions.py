class TransportError(Exception):
    pass


class AddressInUseError(TransportError):
    pass
