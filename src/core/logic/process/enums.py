from src.utils import i18n


class Messages(i18n.TranslatableEnum):
    PROGRAM_LAUNCHED = 'Program launched'
    LAUNCHING = 'Launching...'
    TERMINATING = 'Terminating...'
    PAYLOAD_LOADING_ERROR = 'Failed to load payload, details: {details}'
    HOOK_LOADING_ERROR = 'Failed to load hook, details: {details}'
    HOOK_LOADED = 'Hook loaded: {name} - V{version}'
    PAYLOAD_LOADED = 'Payload loaded: {name} - V{version}'
    TRANSPORT_LAUNCHED = 'Transport launched: {host}:{port}'
    TUNNEL_ESTABLISHED = 'Tunnel established: {url}'
    TRANSPORT_STOPPED = 'Transport stopped'
    TUNNELING_STOPPED = 'Tunneling stopped'
    HOOK_NOT_SUPPORTS_PROTOCOL_ERROR = 'Current hook does not support {protocol} protocol'
    PAYLOAD_NOT_SUPPORTS_PROTOCOL_ERROR = 'Current payload does not support {protocol} protocol'
