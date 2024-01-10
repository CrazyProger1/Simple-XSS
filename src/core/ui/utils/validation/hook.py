from src.core import hooks


def is_valid_hook_path(path: str) -> bool:
    return hooks.is_hook(path)
