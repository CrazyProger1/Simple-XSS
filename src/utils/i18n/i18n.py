from enum import Enum

from .enums import TranslatableEnum
from .. import clsutils


def extract_ids() -> set[str]:
    ids = set()
    for subenum in clsutils.iter_subclasses(TranslatableEnum):
        subenum: Enum

        for item in subenum:
            msgid = item.value
            ids.add(msgid)
    return ids
