from jinja2 import (
    FileSystemLoader,
    Environment
)


def render(directory: str, file: str, **context):
    env = Environment(loader=FileSystemLoader(directory))
    template = env.get_template(file)
    return template.render(**context)