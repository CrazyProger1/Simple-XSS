import argparse

from app.settings import Settings
from app.utils.settings import Format
from config import SETTINGS_FILE


class App:
    def __init__(self, namespace: argparse.Namespace):
        self._args = namespace
        try:
            self._settings = Settings.load(Format.TOML, SETTINGS_FILE)
        except Exception:
            self._settings = Settings()
            self._settings.save(Format.TOML, SETTINGS_FILE)

    @property
    def args(self) -> argparse.Namespace:
        return self._args

    @property
    def settings(self) -> Settings:
        return self._settings

    async def run(self):
        raise NotImplementedError
