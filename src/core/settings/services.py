from pydantic import BaseModel

from typeguard import typechecked

from src.utils import settings as setutil, di
from src.core.config import DEFAULT_SETTINGS_FILE
from src.core.arguments.dependencies import current_arguments
from src.core import arguments
from .dependencies import current_settings, settings_scheme


@typechecked
@di.injector.inject
def load_settings(
        scheme: type[BaseModel] = settings_scheme,
        args: arguments.DefaultArgumentsScheme = current_arguments):
    file = args.settings_file
    try:
        settings = setutil.load(schema=scheme, file=file)
    except (FileNotFoundError, setutil.exceptions.FormatError, ValueError) as e:
        print(e)
        settings = scheme()
        save_settings(settings=settings)

    di.injector.bind(current_settings, settings)
    return settings


@typechecked
@di.injector.inject
def save_settings(
        settings: BaseModel = current_settings,
        args: arguments.DefaultArgumentsScheme = current_arguments):
    file = args.settings_file
    try:
        setutil.save(instance=settings, file=file)
    except ValueError:
        setutil.save(instance=settings, file=DEFAULT_SETTINGS_FILE)
