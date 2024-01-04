from pydantic import BaseModel

from src.utils import settings as setutil, di

from src.core.config import DEFAULT_SETTINGS_FILE
from src.core.dependencies import settings_scheme, current_arguments, current_settings
from src.core.services import arguments


@di.injector.inject
def load_settings(
        scheme: type[BaseModel] = settings_scheme,
        args: arguments.DefaultArgumentsScheme = current_arguments):
    file = args.settings_file
    try:
        settings = setutil.load(schema=scheme, file=file)
    except (FileNotFoundError, setutil.exceptions.FormatError, ValueError):
        settings = scheme()
        setutil.save(instance=settings, file=file)

    di.injector.bind(current_settings, settings)
    return settings


def save_settings(
        settings: BaseModel,
        file: str):
    try:
        setutil.save(instance=settings, file=file)
    except ValueError:
        setutil.save(instance=settings, file=DEFAULT_SETTINGS_FILE)
