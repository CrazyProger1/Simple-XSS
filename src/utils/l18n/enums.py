from enum import Enum


class TranslatableEnum(str, Enum):
    @property
    def value(self) -> str:
        value = super(TranslatableEnum, self).value
        return value

    def __str__(self):
        return self.value
