from .events import BaseEvent
from .enums import TypicalEvent


def is_typical_event(_, event: BaseEvent) -> bool:
    return event.event in TypicalEvent


def is_hi_event(_, event: BaseEvent) -> bool:
    return event.event == TypicalEvent.HI


def is_bye_event(_, event: BaseEvent) -> bool:
    return event.event == TypicalEvent.BYE
