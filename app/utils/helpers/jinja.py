import jinja2
import os
import pathlib
from functools import cache


@cache
def load_env(folder: str) -> jinja2.Environment:
    """Loads Jinja 2 environment"""

    if not os.path.exists(folder):
        raise FileExistsError(f'Folder {folder} does not exist')

    return jinja2.Environment(loader=jinja2.FileSystemLoader(folder))


def get_template(path: str) -> jinja2.Template:
    """Loads Jinja 2 template"""

    file = pathlib.Path(path)
    if not file.exists():
        raise FileExistsError(f'File {file} does not exist')
    elif not file.is_file():
        raise ValueError(f'{file} not a file')

    env = load_env(file.parent)
    return env.get_template(file.name)
