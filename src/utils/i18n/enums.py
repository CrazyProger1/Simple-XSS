import gettext
from enum import Enum


class TranslatableEnum(str, Enum):
    @property
    def value(self) -> str:
        value = super(TranslatableEnum, self).value
        return gettext.gettext(value)

    def __str__(self):
        return self.value
