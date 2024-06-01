from jinja2 import Environment, FileSystemLoader


def render(directory: str, file: str, **context):
    env = Environment(loader=FileSystemLoader(directory))
    template = env.get_template(file)
    return template.render(**context)
