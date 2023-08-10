import colorama
import inspect

from typing import Iterable, Callable
from .printutils import (
    print_question,
    print_pos,
    print_neg
)
from .exceptions import ValidationError


def ask(
        prompt: str,
        default: any = None,
) -> str:
    print_question(prompt)
    value = input('[>] ')

    return value or default


def ask_validated(
        prompt: str,
        validator: Callable[[str], bool | None],
        default: any = None,
):
    value = ask(
        prompt=prompt,
        default=default
    )
    try:
        if not validator(value):
            raise ValidationError
        return value
    except ValidationError as e:
        print_neg(str(e) or 'Value is invalid')
        return ask_validated(
            prompt=prompt,
            validator=validator,
            default=default
        )


def ask_bool(prompt: str, default: bool = False):
    value = ask(
        prompt=prompt,
        default=default
    )

    return value and str(value).lower() in {'1', 'y', 'yes', 'true', 't', True}


def ask_option(
        prompt: str,
        options: Iterable,
        default: any = None
) -> str:
    if not isinstance(options, Iterable):
        raise ValueError('options must be iterable')

    option_tuple = tuple(options)

    print_question(prompt)

    for i, option in enumerate(option_tuple):
        print(f'[{i}]', option)

    value = input('[>] ')

    if not value:
        return default

    if value.isdigit():
        index = abs(int(value))
        if len(option_tuple) > index:
            return option_tuple[index]

    elif value in option_tuple:
        return value

    return default
