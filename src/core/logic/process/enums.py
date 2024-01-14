from src.utils import l18n


class Messages(l18n.TranslatableEnum):
    PROGRAM_LAUNCHED = 'Program launched'
    LAUNCHING = 'Launching...'
    TERMINATING = 'Terminating...'
    PAYLOAD_LOADING_ERROR = 'Failed to load payload, details: {details}'
    HOOK_LOADING_ERROR = 'Failed to load hook, details: {details}'
